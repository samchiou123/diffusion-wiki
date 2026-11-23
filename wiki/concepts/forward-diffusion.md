# 正向擴散（Forward diffusion）

## 白話概念

依固定排程逐步加入高斯雜訊，也可直接得到指定時間步的含雜訊影像。[S01-C01]

## 與其他概念的關係

產生的含雜訊影像是 [雜訊預測](noise-prediction.md) 的輸入；[生成](reverse-sampling.md) 則從隨機雜訊出發。[S01-C02] [S01-C03]

## 來源與待補

依據：[DDPM 主張表](../sources/ddpm.md)。排程改良見 [雜訊排程](noise-schedule.md)；記號差異見 [公式記號比較](../comparisons/notation.md)。

[返回目錄](../index.md)
