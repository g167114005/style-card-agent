# 第 12 週作業：統一風格圖像產生的 Agent

北醫 G167114005 醫學院人工智慧醫療碩士在職專班 碩二 鄭為遠
系列：**看懂中風 AI 教學圖卡**；風格：**病歷夾手繪衛教風**；吉祥物：**腦腦醫師 Dr. NAO**
作品頁：https://g167114005.github.io/style-card-agent/

## 作品（同一風格，共 4 張）
| 角色設定圖 | ① NIHSS | ② Grad-CAM | ③ SHAP |
|---|---|---|---|
| ![](style/ref/mascot.png) | ![](output/01_NIHSS.png) | ![](output/02_GradCAM.png) | ![](output/03_SHAP.png) |

每張圖卡上的文字和 `html/` 裡同名的 HTML 逐字相同，可直接打開 HTML 核對；更完整的內容與出處在 `notes/`。

## 製作流程
```
notes/*.md ──skill: notes-to-html──▶ html/*.html ──skill: html-to-png──▶ output/*.png
 內容筆記                             一頁式網頁：只有內容、沒有插圖        一頁式教學圖卡
```
1. **定風格**（一次）：把色票、版型、筆觸、吉祥物和禁止事項寫成 `style/STYLE.md`。第 7 節是給模型的英文風格描述，每次生圖都原文貼上。
2. **notes → html**（skill `skills/notes-to-html`）：把內容筆記濃縮成固定版型的 HTML，包括標題、副標、①②③ 三塊、對話框、頁腳，每格都有字數上限。文字只在這一步決定。
3. **組 prompt**：`tools/gen_card.py` 解析 HTML，把「風格合約＋版型＋逐字文字」組成 prompt，存在 `prompts/`。
4. **生圖（本次實際做法：ChatGPT 桌面 App）**：agent 在同一個 ChatGPT 對話裡依序貼上 4 段 prompt。
   - 第 1 段畫角色設定圖。
   - 第 2–4 段畫圖卡，開頭都要求「沿用本對話上面那張角色設定圖」，靠對話上下文維持角色一致，不必再重新附圖。
   - 過程截圖在 `screenshots/`。
5. **QC**：逐字對照 HTML，並檢查版型、角色和色票。本次 4 張都一次通過，見 `logs/qc.md`。

### 設計目的：為什麼這樣「預期」能統一風格
- **風格與內容分離**：風格只寫在 STYLE.md，內容只寫在 HTML，每次生圖都用同一份描述，不靠臨場形容。
- **同一張角色設定圖當參考**：目的是讓吉祥物在每張圖卡長得一樣。
- **固定版型與字數上限**：目的是讓版面一致，並減少中文錯字。

以上是設計目的，不是保證。本次只生成一輪，觀察到的結果是 3 張圖卡文字全對、角色和版型一致。我們沒有做不同字數或有無參考圖的對照實驗。

## 怎麼重現
**ChatGPT App 版（本次做法）**：開一個新對話，依序貼上下列 prompt，並把生成的圖片存成右欄的檔名：

| 順序 | 貼上的 prompt | 圖片存成 |
|---|---|---|
| 1 | `prompts/00_mascot.txt` | `style/ref/mascot.png` |
| 2 | `prompts/01_NIHSS.txt` | `output/01_NIHSS.png` |
| 3 | `prompts/02_GradCAM.txt` | `output/02_GradCAM.png` |
| 4 | `prompts/03_SHAP.txt` | `output/03_SHAP.png` |

**API 版（程式已寫好，本次沒有執行）**：用 Windows 的 PowerShell 開啟本資料夾，依序執行下面兩行。第一行只在目前視窗設定金鑰；也可以改在本資料夾建立 `.env`，內容寫 `OPENAI_API_KEY=sk-...`，這個檔案已列入 gitignore。
```powershell
$env:OPENAI_API_KEY = "sk-..."
.\run_all.bat
```
只看 prompt、不呼叫 API：
```powershell
python tools/gen_card.py html/01_NIHSS.html --dry-run
```
注意事項：
- **模型**：`gpt-image-1` 已於 2026-10-23 停用（見 [OpenAI 停用公告](https://developers.openai.com/api/docs/deprecations)）。請先用環境變數 `IMAGE_MODEL` 指定目前支援的影像模型，例如 `$env:IMAGE_MODEL = "gpt-image-2.5-flare"`。程式預設也已改成這個模型，但還沒實際呼叫測試過。
- **重跑**：輸出檔已存在時，舊檔會依序改名為 `_v1`、`_v2`…，不會被覆蓋。要修正錯字，可加 `--fix "第②塊的『xx』應為『yy』"`。
- **失敗時**：API 回傳錯誤時，程式會印出錯誤碼與訊息並結束，不寫 log、不存圖。`run_all.bat` 遇到第一個錯誤就停止，後面的圖不會繼續跑。
- 只用 Python 標準函式庫，不需要另外安裝套件。

## 檔案
```
AGENTS.md                 agent 規則
style/STYLE.md            風格合約；style/ref/mascot.png 角色設定圖
skills/notes-to-html/     skill 1
skills/html-to-png/       skill 2
tools/gen_card.py         組 prompt／呼叫 OpenAI API 的程式
notes/ html/ output/      三個階段的產物
prompts/                  實際送給 GPT 的完整 prompt
screenshots/              呼叫 GPT 生圖的過程截圖
logs/                     QC 紀錄（API 版另有每次呼叫的 JSON）
```

## 內容出處
- Grad-CAM、SHAP：Cheng W-Y, Lin H-Y, Tsai Y-J, Ko C-H. Explainable AI for Acute Ischemic Stroke Neuroimaging: A Critical Review of SHAP and Grad-CAM Applications and Their Methodological Limitations. *Diagnostics* 2026;16(22):3833. doi:10.3390/diagnostics16223833。各句對應的章節標在 `notes/02_GradCAM.md`、`notes/03_SHAP.md`。
- 白話解釋改寫自作者第 10 週作業的 wiki：https://g167114005.github.io/xai-stroke-llm-wiki/wiki-site/index.html （`concepts/grad-cam`、`concepts/shap`、`concepts/stroke-terms`）。
- NIHSS：NINDS NIH Stroke Scale，11 個評估項目，總分 0–42（[Radiopaedia: NIHSS](https://radiopaedia.org/articles/nihss)）。
