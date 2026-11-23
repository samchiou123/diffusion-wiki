# 方法比較：三個改良方向可以分開看

以下是 AI 依本次五份資料整理的入門比較，不是相同資料集、硬體與訓練條件下的效能排行。

| 方法 | 核心角色或改動 | 入門時保留的條件 | 依據 |
|---|---|---|---|
| DDPM | 雜訊預測訓練與逐步隨機取樣的基礎範例 | 本文採固定反向變異數及特定步數，不當成所有擴散模型的定義 | [S01-C02] [S01-C03] [S01-C05] [S01-C06] |
| DDIM | 沿用訓練網路、改取樣路徑與更新式 | η=0 且固定初始雜訊及設定時為確定性；步數與品質有取捨 | [S02-C01] [S02-C02] [S02-C03] |
| Improved DDPM | 變異數學習、混合目標、雜訊排程與較少步數取樣 | 不把 cosine、變異數學習、DDIM 混稱為同一項改動 | [S03-C01] [S03-C02] [S03-C03] [S03-C04] |
| Latent Diffusion | 在學得的潛在表示中做擴散，再解碼成影像 | 壓縮存在細節準確性限制；可與 DDIM 取樣結合 | [S04-C01] [S04-C02] [S04-C04] [S04-C05] |

## 教學結論

「改取樣方法」「改訓練與排程」「改表示空間」是本次比較的三個軸。不能畫成 DDPM 被 DDIM 取代、再被 LDM 取代的單一路線。這是根據來源差異的 AI 教學整理。

來源：[DDPM](../sources/ddpm.md)、[DDIM](../sources/ddim.md)、[Improved DDPM](../sources/improved-ddpm.md)、[Latent Diffusion](../sources/latent-diffusion.md)。教學背景見 [生成模型](../concepts/generative-models.md)。

[返回目錄](../index.md)
