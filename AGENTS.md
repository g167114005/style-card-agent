# AGENTS.md — 統一風格圖像產生 Agent 員工手冊

> Claude Code 使用者：`CLAUDE.md` 只寫 `@AGENTS.md`。

## 1. 這個 agent 做什麼
把一個主題的**內容筆記**，變成一張**風格固定**的單張教學圖卡（PNG）。系列名稱「看懂中風 AI 教學圖卡」，讀者是沒有醫療背景的同學。

## 2. 流程（三個資料夾、兩個 skill）
```
notes/*.md  ──(skill: notes-to-html)──▶  html/*.html  ──(skill: html-to-png)──▶  output/*.png
 內容筆記                                   一頁式網頁版：只有內容、沒有插圖        一頁式教學圖卡
```
- 內容（文字）只在 notes → html 這一步決定；生圖那一步**不准改字**。
- 風格只寫在 `style/STYLE.md`；生圖時一律附上吉祥物設定圖 `style/ref/mascot.png`。

## 3. 規則
1. 新主題：先寫 `notes/NN_主題.md`，再照 `skills/notes-to-html/SKILL.md` 產生 html。
2. 生圖：照 `skills/html-to-png/SKILL.md` 執行 `python tools/gen_card.py html/NN_主題.html`。
3. 每次呼叫 GPT 都會在 `logs/` 留一筆紀錄（模型、參數、完整 prompt、耗時），不得刪除。
4. 生圖後逐項檢查（見 html-to-png 的 QC 清單）；不合格就重跑，最多 3 次，並在 `logs/qc.md` 記錄。
5. 金鑰只從環境變數 `OPENAI_API_KEY` 或本機 `.env` 讀取；`.env` 已列入 `.gitignore`，永遠不進版控、不印到螢幕。

## 4. 內容正確性
- 醫學與 XAI 內容取自作者已刊登的 review（*Diagnostics* 2026, 16, 3833）與第 10 週 wiki；NIHSS 為公開量表。
- 圖卡字數少，只放「回頭查得到」的重點；不確定的數字不放。
