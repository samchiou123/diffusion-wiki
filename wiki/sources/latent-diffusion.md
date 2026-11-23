# S04：High-Resolution Image Synthesis with Latent Diffusion Models

- 作者：Robin Rombach、Andreas Blattmann、Dominik Lorenz、Patrick Esser、Björn Ommer。
- 發表／版本：CVPR 2022；本次使用 arXiv v2。
- 原始來源：[版本頁](https://arxiv.org/abs/2112.10752)；[本機 PDF](https://arxiv.org/abs/2112.10752)。
- 取得及整理日期：2026-11-23。
- 狀態：已 ingest 與入門主題相關的內容；使用者閱讀待完成。
- 閱讀範圍：PDF 第 1、3–5、9 頁；第 4 頁 Figure 3 與方法已看原頁圖像。未逐一核對其餘附錄、所有任務及指標。

## 入門摘要

改變的是擴散工作的表示空間。訓練時編碼原圖和生成時解碼新潛在樣本，要分開說明。

## 可回查主張

| 主張 ID | 作者內容的白話整理與 AI 界線 | 原文定位 |
|---|---|---|
| S04-C01 | 先以學得的編碼器／解碼器建立較低維度表示，再在該潛在空間訓練擴散模型，以降低運算負擔。 | 第 3、3.1–3.2 節；PDF 第 3–4 頁。 |
| S04-C02 | 時間條件 U-Net 在潛在表示上進行雜訊預測；生成的潛在樣本最後經解碼器轉成影像。 | 第 3.2 節式 (2)、Figure 3；PDF 第 4 頁。 |
| S04-C03 | 可透過條件編碼及 cross-attention 接入文字等條件，以控制合成內容。 | 第 3.3 節、Figure 3、式 (3)；PDF 第 4–5 頁。 |
| S04-C04 | 壓縮重建能力會限制需高像素精度的任務；較低成本不等於所有細節完全保留。 | 第 5 節 Limitations；PDF 第 9 頁。 |
| S04-C05 | 作者在部分模型比較中使用 DDIM 取樣器；潛在擴散與 DDIM 可以結合。 | 第 4.1 節、Figure 7 討論；PDF 第 5 頁。 |

## 限制與待確認

未重現論文模型，也不據此推論超音波、FPGA 或臨床結果。個人心得待補。

## 連到知識網絡
- [潛在表示](../concepts/latent-representation.md)
- [條件生成](../concepts/conditional-generation.md)
- [U-Net 的角色](../concepts/unet-role.md)

[返回 Wiki 目錄](../index.md)
