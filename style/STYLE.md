# STYLE.md — 「病歷夾手繪衛教風」風格規格

> 這份檔案是整個專案的「風格合約」。每一次呼叫 GPT 生圖，`tools/gen_card.py` 都會把下面「給模型的風格描述」整段原封不動放進 prompt，並附上吉祥物設定圖 `style/ref/mascot.png` 當參考圖。
> 要改風格，只改這一份；不要在個別 prompt 裡各自加形容詞。

## 1. 系列名稱
看懂中風 AI 教學圖卡

## 2. 吉祥物：腦腦醫師（Dr. NAO）
- 圓滾滾的粉紅色「大腦」造型小角色，大腦皺褶線條簡化成幾條柔和的弧線
- 頭頂戴淺藍色手術帽，脖子掛銀色聽診器，穿白色小醫師袍
- 圓黑豆眼、粉色腮紅、小小的微笑；短短的手腳
- 每張圖卡都要出現一次，旁邊配一個對話框

## 3. 色票
| 用途 | 色名 | HEX |
|---|---|---|
| 背景紙 | 米白方格紙 | #FBF7EE |
| 主色 1 | 薄荷綠 | #8FD3C1 |
| 主色 2 | 嬰兒藍 | #9CC9E8 |
| 強調 | 蜜桃粉 | #F6B8B8 |
| 便利貼 | 奶油黃 | #FBE7A1 |
| 文字 | 深藏青 | #2F3E5C |
| 警示 | 珊瑚紅 | #E8736C |

## 4. 版型（直式 2:3，1024 × 1536）
1. **頂部**：一條膠囊形小標籤寫系列名稱；下面是用紙膠帶貼著的大標題橫幅＋一行副標。
2. **中段**：三個圓角便利貼區塊，左上角各有圓形編號徽章 ①②③，每塊一個小標題＋一兩行說明，旁邊配一個簡單手繪小插圖。
3. **右下**：腦腦醫師＋對話框（一句重點）。
4. **底部**：細細的頁腳列，左邊作者、右邊頁碼（例如 1/3）。

## 5. 筆觸與質感
- 手繪細線邊框、輕微水彩暈染、粉彩配色、柔和陰影
- 點綴：紙膠帶、小星星、醫療十字、迴紋針，數量克制
- 字體感：標題粗圓體、內文清楚的黑體；**所有文字必須是繁體中文，逐字照抄指定內容**

## 6. 禁止
- 不要寫實照片風、不要 3D 金屬光澤、不要暗色背景
- 不要出現真實醫院、廠牌、他人角色或 logo
- 不要出現血腥或真實病人影像；腦部影像一律畫成簡化示意圖
- 不要自行增加指定以外的文字

## 7. 給模型的風格描述（gen_card.py 會原文貼進 prompt）
```
STYLE: "Clinical-clipboard hand-drawn health-education card" (病歷夾手繪衛教風).
Cream grid-notebook paper (#FBF7EE) clipped onto a light-wood clinical clipboard.
Soft pastel palette: mint green #8FD3C1, baby blue #9CC9E8, peach pink #F6B8B8, butter yellow #FBE7A1,
text in deep navy #2F3E5C, warning accents in coral red #E8736C.
Thin hand-drawn outlines, light watercolor wash, gentle shadows, washi tape, tiny stars and medical crosses used sparingly.
Rounded sticky-note panels with circular number badges. Bold rounded headline lettering, clean sans-serif body text.
Mascot "Dr. NAO": a chubby pink brain-shaped character with simplified soft folds, light-blue surgical cap,
silver stethoscope, small white doctor's coat, black bean eyes, pink blush, tiny smile, short arms and legs
— must match the reference mascot image exactly.
No photorealism, no 3D chrome, no dark background, no real logos or brands, no gore, no real patient images.
All text must be Traditional Chinese, copied character-by-character exactly as given; add no other text.
```
