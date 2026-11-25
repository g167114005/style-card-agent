# SHAP（Shapley Additive exPlanations）

- 比喻：小組分功勞。讓每個組員輪流加入或拿掉，看成績變多少，平均後就是每個人的貢獻（wiki `concepts/shap.md`）。
- 套到模型：組員＝輸入特徵（年齡、梗塞體積、影像紋理…），成績＝模型預測；SHAP 值＝這個特徵把這次預測往上推或往下拉多少。
- 回答的是「這個模型怎麼用這些特徵」，不是「這個特徵在人體裡造成什麼」。
- 要小心（review）：
  - 特徵彼此高度相關時，個別排名會隨算法設定改變（wiki `issues/shap-feature-dependence.md`）。
  - 排名高不代表有額外預測價值（wiki `issues/shap-rank-vs-incremental-value.md`）。
  - Review 評讀的 SHAP 研究 20 篇，沒有一篇交代 background distribution（review §4.4）。
