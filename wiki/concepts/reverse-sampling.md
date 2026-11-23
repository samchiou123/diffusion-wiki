# 反向取樣（Reverse sampling）

## 白話概念

DDPM 無條件生成從高斯雜訊開始，逐步更新，最後得到樣本。中間步驟仍包含隨機項。[S01-C03]

## 與其他概念的關係

使用已訓練的 [預測網路](noise-prediction.md)；可對照 [訓練與生成](../comparisons/training-vs-generation.md)。原論文實驗採 1000 步，不能當成普遍定義。[S01-C02] [S01-C05]

## 來源與待補

依據：[DDPM 主張表](../sources/ddpm.md)。跨方法差異見 [方法比較](../comparisons/diffusion-methods.md)。

[返回目錄](../index.md)

## S02 新增的來源觀點

重點是訓練與取樣可以分開設計。減少取樣成本仍有品質與設定條件，不採用無條件的加速倍數宣稱。

來源入口：[S02 主張表](../sources/ddim.md)。本輪來源主張：[S02-C01] [S02-C02] [S02-C03] [S02-C04]

## S03 新增的來源觀點

改良包含排程、訓練目標、變異數和取樣設定；不宜簡化成把 DDPM 換成 DDIM。

來源入口：[S03 主張表](../sources/improved-ddpm.md)。本輪來源主張：[S03-C01] [S03-C02] [S03-C03] [S03-C04]
