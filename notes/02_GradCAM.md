# Grad-CAM（Gradient-weighted Class Activation Mapping）

- 在 CT／MRI 上疊一張熱圖；越紅代表模型做判斷時越依賴那一塊（wiki `concepts/grad-cam.md`）。
- 原理：從最後一層卷積特徵往回算梯度，得到每個特徵格子的重要性，再把這張粗格子圖內插放大貼回原圖。
- 只能回答「模型看了哪裡」，不能回答「模型看對了沒」。
- 三個弱點（review §4.2）：
  1. 解析度粗：熱圖本質是被放大的粗格子圖，畫不出半影細緻邊界。
  2. 怕假影：NCCT 顱骨旁 beam-hardening、DWI 磁化率失真都會造成假亮區。
  3. 看不到非影像變項：發病到院時間、血糖、入院 NIHSS 都無法呈現。
- Review 評讀的影像顯著圖研究 10 篇，定位全靠肉眼、沒有量化（review §4.4）。
