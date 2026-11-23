# 雜訊排程（Noise schedule）

## 白話概念

排程決定各時間步的訊號與雜訊比例如何變化。原始 DDPM 採固定的正向過程；Improved DDPM 提出 cosine 排程改變訊號消失的節奏。[S01-C01] [S03-C02]

## 教學界線

「線性 β 排程」不等於影像外觀或累積訊號量隨時間線性變化。不同排程與取樣步數要分開描述；跨文記號見 [公式記號比較](../comparisons/notation.md)。以上為依來源公式的 AI 教學整理。

依據：[DDPM](../sources/ddpm.md)、[Improved DDPM](../sources/improved-ddpm.md)。

[返回目錄](../index.md)
