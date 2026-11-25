# 第 12 週作業：統一風格圖像產生的 Agent

北醫 G167114005 醫學院人工智慧醫療碩士在職專班 碩二 鄭為遠
系列：**看懂中風 AI 教學圖卡**；風格：**病歷夾手繪衛教風**；吉祥物：**腦腦醫師 Dr. NAO**

## 作品（同一風格，共 4 張）
| 角色設定圖 | ① NIHSS | ② Grad-CAM | ③ SHAP |
|---|---|---|---|
| ![](style/ref/mascot.png) | ![](output/01_NIHSS.png) | ![](output/02_GradCAM.png) | ![](output/03_SHAP.png) |

## 製作流程
```
notes/*.md ──skill: notes-to-html──▶ html/*.html ──skill: html-to-png──▶ output/*.png
 內容筆記                             一頁式網頁：只有內容、沒有插圖        一頁式教學圖卡
```
1. **定風格**（一次）：把色票、版型、筆觸、吉祥物、禁止事項寫成 `style/STYLE.md`。第 7 節是給模型的英文風格描述，每次生圖都原文貼上。
2. **定角色**（一次）：`python tools/gen_card.py --mascot` 呼叫 GPT 影像模型（`/v1/images/generations`），畫出吉祥物設定圖 `style/ref/mascot.png`。
3. **notes → html**（skill `skills/notes-to-html`）：把內容筆記濃縮成固定版型 HTML：標題、副標、三塊 ①②③、對話框、頁腳，每格有字數上限。文字只在這一步決定。
4. **html → png**（skill `skills/html-to-png`）：`tools/gen_card.py` 解析 HTML，把「風格合約＋版型＋逐字文字」組成 prompt，附上吉祥物設定圖當參考圖，呼叫 `/v1/images/edits`（gpt-image-1，1024×1536，quality=high）。
5. **QC**：逐字核對、檢查版型與角色一致；不合格就加 `--fix` 重跑，舊版自動保留為 `_v1`。
6. **紀錄**：每次呼叫 GPT 都在 `logs/` 留一筆 JSON，內容包括模型、端點、參數、完整 prompt、耗時與 token 用量。

### 為什麼這樣能「統一風格」
- **風格與內容分離**：風格只寫在 STYLE.md，內容只寫在 HTML，兩者都不靠臨場發揮。
- **參考圖鎖角色**：每張圖卡都把同一張吉祥物設定圖傳給模型。
- **固定版型與字數上限**：版面一致，字少也讓模型比較不會寫錯中文。

## 怎麼跑
**ChatGPT App 版**：依序把 `prompts/00_mascot.txt`、`01`、`02`、`03` 貼進同一個 ChatGPT 對話，下載圖片後放進 `style/ref/` 與 `output/`。

**API 版**：
```
setx OPENAI_API_KEY "sk-..."      :: 或在本資料夾建 .env（已 gitignore）
run_all.bat                       :: 依序產生吉祥物與三張圖卡
python tools/gen_card.py html/01_NIHSS.html --dry-run   :: 只看 prompt
```
只用 Python 標準函式庫，不需要另外安裝套件。

## 檔案
```
AGENTS.md                 agent 規則
style/STYLE.md            風格合約；style/ref/mascot.png 吉祥物設定圖
skills/notes-to-html/     skill 1
skills/html-to-png/       skill 2
tools/gen_card.py         生圖程式（呼叫 OpenAI API）
notes/ html/ output/      三個階段的產物
prompts/                  實際送給 GPT 的完整 prompt
screenshots/              呼叫 GPT 生圖的過程截圖
logs/                     QC 紀錄（API 版另有每次呼叫的 JSON）
```

內容出處：作者已刊登的 review（*Diagnostics* 2026, 16, 3833）與第 10 週 wiki；NIHSS 為公開量表。
