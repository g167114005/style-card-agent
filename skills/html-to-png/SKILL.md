---
name: html-to-png
description: 讀取固定版型的 HTML，組成「風格合約＋逐字內容＋版型」prompt，附上吉祥物參考圖，呼叫 OpenAI GPT 影像模型生成直式教學圖卡 PNG。
---

# html → png

## 兩種執行方式
- **ChatGPT App**（沒有 API 金鑰時）：`python tools/gen_card.py <html> --dry-run` 印出 prompt，存進 `prompts/`。在同一個 ChatGPT 對話裡依序貼上：先貼吉祥物，再貼三張圖卡（圖卡 prompt 開頭要求「沿用上面角色設定圖」）。下載圖片後放進 `style/ref/` 與 `output/`，並截下過程。
- **API**：照下面的步驟執行。

## 前置（只做一次）
1. 設好金鑰：PowerShell `setx OPENAI_API_KEY "sk-..."`（重開視窗生效），或在專案根目錄建 `.env`：`OPENAI_API_KEY=sk-...`
2. 先產生吉祥物設定圖（之後每張都拿它當參考圖）：
   ```
   python tools/gen_card.py --mascot
   ```
   檢查 `style/ref/mascot.png` 滿意後才繼續。

## 生一張圖卡
```
python tools/gen_card.py html/01_NIHSS.html
python tools/gen_card.py html/01_NIHSS.html --dry-run   # 只印出 prompt，不呼叫 API
```

## gen_card.py 做的事
1. 解析 html 的 `data-*` 欄位，取得標題、三塊內容、對話框、頁腳、小插圖描述。
2. 組 prompt：`STYLE.md` 第 7 節原文 ＋ 版型（STYLE.md 第 4 節）＋ 逐字文字清單。
3. 呼叫 `POST /v1/images/edits`，把 `style/ref/mascot.png` 當參考圖，`size=1024x1536`、`quality=high`。
4. 存到 `output/NN_主題.png`；若檔名已存在，舊檔改名為 `_v1`、`_v2`…保留。
5. 在 `logs/` 寫一筆 JSON：時間、模型、端點、參數、完整 prompt、耗時、token 用量。

## QC 清單（每張都要過）
- [ ] 所有文字與 html 逐字相同，沒有錯字、漏字、簡體字、亂碼
- [ ] 版型：頂部膠囊＋大標題、三塊編號便利貼、右下吉祥物＋對話框、底部頁腳
- [ ] 吉祥物與 `mascot.png` 同一個角色（粉紅大腦、淺藍手術帽、聽診器、白袍）
- [ ] 色票與筆觸跟前幾張一致；沒有寫實照片或暗色背景
- [ ] 沒有多出來的文字或 logo

不合格：在 `logs/qc.md` 寫原因，重跑（最多 3 次）。只有個別字錯時，可在 prompt 末尾加 `--fix "第②塊的『xx』寫錯，應為『yy』"` 再跑一次。
