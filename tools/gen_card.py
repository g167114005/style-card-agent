#!/usr/bin/env python3
"""統一風格圖卡生成器：html → png（呼叫 OpenAI GPT 影像模型）。

只用 Python 標準函式庫，不需 pip install。

用法：
  python tools/gen_card.py --mascot                 # 先產生吉祥物設定圖 style/ref/mascot.png
  python tools/gen_card.py html/01_NIHSS.html       # 產生一張圖卡 → output/01_NIHSS.png
  python tools/gen_card.py html/01_NIHSS.html --dry-run
  python tools/gen_card.py html/01_NIHSS.html --fix "第②塊的『xx』寫錯，應為『yy』"
環境變數：
  OPENAI_API_KEY   必填（或寫在專案根目錄 .env）
  IMAGE_MODEL      選填，預設 gpt-image-2.5-flare（gpt-image-1 已停用）
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLE_MD = ROOT / "style" / "STYLE.md"
MASCOT = ROOT / "style" / "ref" / "mascot.png"
OUT_DIR = ROOT / "output"
LOG_DIR = ROOT / "logs"
API = "https://api.openai.com/v1"
MODEL = os.environ.get("IMAGE_MODEL", "gpt-image-2.5-flare")  # gpt-image-1 已於 2026-10-23 停用

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------- 讀風格合約 ----------
def style_block() -> str:
    text = STYLE_MD.read_text(encoding="utf-8")
    m = re.search(r"## 7\..*?```\n(.*?)```", text, re.S)
    if not m:
        sys.exit("STYLE.md 第 7 節找不到風格描述")
    return m.group(1).strip()


# ---------- 解析 html ----------
class CardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.fields, self.icons = [], {}, {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "data-icon" in a and "data-n" in a:
            self.icons[a["data-n"]] = a["data-icon"]
        f = a.get("data-field")
        self.stack.append(f)
        if f:
            self.fields.setdefault(f, "")

    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        for f in self.stack:
            if f:
                self.fields[f] += data


def parse_card(path: Path) -> dict:
    p = CardParser()
    p.feed(path.read_text(encoding="utf-8"))
    f = {k: " ".join(v.split()) for k, v in p.fields.items()}
    need = ["series", "title", "subtitle", "bubble", "author", "page"]
    need += [f"b{i}-{x}" for i in (1, 2, 3) for x in ("head", "body")]
    miss = [k for k in need if not f.get(k)]
    if miss:
        sys.exit(f"{path.name} 缺欄位：{miss}")
    f["icons"] = p.icons
    return f


# ---------- 組 prompt ----------
def card_prompt(c: dict, fix: str | None) -> str:
    blocks = "\n".join(
        f"  Panel {i} (badge {'①②③'[i-1]}): heading 「{c[f'b{i}-head']}」, body 「{c[f'b{i}-body']}」; "
        f"small doodle beside it: {c['icons'].get(str(i), 'a simple related doodle')}."
        for i in (1, 2, 3)
    )
    p = f"""Create ONE vertical 2:3 single-page teaching card (portrait).

{style_block()}

LAYOUT (top to bottom, keep exactly this structure):
- Top: small rounded pill label with text 「{c['series']}」.
- Below it: big headline banner held by washi tape, headline 「{c['title']}」, one-line subtitle 「{c['subtitle']}」.
- Middle: three rounded pastel sticky-note panels stacked vertically, each with a circular number badge:
{blocks}
- Bottom-right: the mascot Dr. NAO (same character as the reference image) with a speech bubble 「{c['bubble']}」.
- Footer strip: left 「{c['author']}」, right 「{c['page']}」.

TEXT RULES: render every quoted Traditional Chinese string exactly, character by character, clearly legible;
do not translate, do not add any other words."""
    if fix:
        p += f"\n\nCORRECTION FROM LAST RUN: {fix}"
    return p


def mascot_prompt() -> str:
    return f"""Create a character design sheet (landscape) for an original mascot.

{style_block()}

SHEET CONTENT: the mascot Dr. NAO shown in front view, side view and back view in a row,
plus three small expression heads below: happy, thinking, surprised.
Clean cream grid-paper background, pastel colour swatches of the palette in one corner.
Only text allowed on the sheet: 「腦腦醫師 Dr. NAO」 as the title."""


# ---------- HTTP ----------
def api_key() -> str:
    k = os.environ.get("OPENAI_API_KEY", "").strip()
    env = next((ROOT / n for n in (".env", ".env.txt") if (ROOT / n).exists()), None)
    if not k and env:
        for line in env.read_text(encoding="utf-8-sig").splitlines():
            if line.strip().startswith("OPENAI_API_KEY"):
                k = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not k:
        sys.exit("找不到 OPENAI_API_KEY（環境變數或 .env）")
    return k


def post(url: str, body: bytes, ctype: str) -> dict:
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": f"Bearer {api_key()}", "Content-Type": ctype})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"API 錯誤 {e.code}：{e.read().decode('utf-8', 'replace')[:800]}")


def generate(prompt: str, size: str) -> tuple[dict, dict]:
    params = {"model": MODEL, "prompt": prompt, "size": size, "quality": "high", "n": 1}
    return post(f"{API}/images/generations", json.dumps(params).encode(), "application/json"), \
        {"endpoint": "images/generations", **{k: v for k, v in params.items() if k != "prompt"}}


def edit(prompt: str, size: str, refs: list[Path]) -> tuple[dict, dict]:
    params = {"model": MODEL, "prompt": prompt, "size": size, "quality": "high", "n": "1"}
    b = uuid.uuid4().hex
    parts = []
    for k, v in params.items():
        parts.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    for r in refs:
        parts.append(f'--{b}\r\nContent-Disposition: form-data; name="image[]"; filename="{r.name}"\r\n'
                     f"Content-Type: image/png\r\n\r\n".encode() + r.read_bytes() + b"\r\n")
    parts.append(f"--{b}--\r\n".encode())
    meta = {"endpoint": "images/edits", "reference_images": [str(r.relative_to(ROOT)) for r in refs],
            **{k: v for k, v in params.items() if k != "prompt"}}
    return post(f"{API}/images/edits", b"".join(parts), f"multipart/form-data; boundary={b}"), meta


# ---------- 存檔與紀錄 ----------
def save_png(resp: dict, out: Path) -> None:
    try:
        data = base64.b64decode(resp["data"][0]["b64_json"])
    except (KeyError, IndexError, TypeError, ValueError):
        sys.exit(f"API 回應沒有圖片資料：{json.dumps(resp, ensure_ascii=False)[:500]}")
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        n = 1
        while (bak := out.with_name(f"{out.stem}_v{n}{out.suffix}")).exists():
            n += 1
        out.rename(bak)
        print(f"  舊檔保留為 {bak.relative_to(ROOT)}")
    out.write_bytes(data)


def write_log(name: str, meta: dict, prompt: str, secs: float, resp: dict, out: Path) -> Path:
    LOG_DIR.mkdir(exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    log, n = LOG_DIR / f"{ts}_{name}.json", 1
    while log.exists():
        n += 1
        log = LOG_DIR / f"{ts}_{name}_{n}.json"
    log.write_text(json.dumps({
        "time": dt.datetime.now().isoformat(timespec="seconds"), **meta,
        "seconds": round(secs, 1), "usage": resp.get("usage"),
        "output": str(out.relative_to(ROOT)), "prompt": prompt,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return log


def main():
    ap = argparse.ArgumentParser(description="統一風格圖卡生成器")
    ap.add_argument("html", nargs="?", help="html/NN_主題.html")
    ap.add_argument("--mascot", action="store_true", help="產生吉祥物設定圖")
    ap.add_argument("--dry-run", action="store_true", help="只印 prompt，不呼叫 API")
    ap.add_argument("--fix", help="上一版的修正說明，附加到 prompt 末尾")
    a = ap.parse_args()

    if a.mascot:
        name, out, size = "mascot", MASCOT, "1536x1024"
        prompt = mascot_prompt()
    elif a.html:
        src = (ROOT / a.html) if not Path(a.html).is_absolute() else Path(a.html)
        name, out, size = src.stem, OUT_DIR / f"{src.stem}.png", "1024x1536"
        prompt = card_prompt(parse_card(src), a.fix)
    else:
        ap.error("請給 html 檔或 --mascot")

    print("=" * 64)
    print(f" 統一風格圖卡 Agent｜{name}｜模型 {MODEL}｜{size}")
    print("=" * 64)
    print(prompt)
    print("-" * 64)
    if a.dry_run:
        print("（dry-run：未呼叫 API）")
        return

    api_key()
    print(" 已讀取 OPENAI_API_KEY（不顯示）")
    t0 = time.time()
    if a.mascot:
        print(" 呼叫 POST /v1/images/generations …（約 1 分鐘）")
        resp, meta = generate(prompt, size)
    else:
        if not MASCOT.exists():
            sys.exit("請先執行 python tools/gen_card.py --mascot")
        print(" 呼叫 POST /v1/images/edits（附吉祥物參考圖）…（約 1–2 分鐘）")
        resp, meta = edit(prompt, size, [MASCOT])
    secs = time.time() - t0
    save_png(resp, out)
    log = write_log(name, meta, prompt, secs, resp, out)
    print(f" 完成：{out.relative_to(ROOT)}（{secs:.0f} 秒）")
    print(f" 紀錄：{log.relative_to(ROOT)}")
    if resp.get("usage"):
        print(f" usage：{json.dumps(resp['usage'], ensure_ascii=False)}")


if __name__ == "__main__":
    main()
