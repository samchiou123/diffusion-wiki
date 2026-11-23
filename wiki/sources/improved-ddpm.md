# S03：Improved Denoising Diffusion Probabilistic Models

- 作者：Alex Nichol、Prafulla Dhariwal。
- 發表／版本：2021；本次使用 arXiv v1，正式 ICML 2021 書目另見來源頁。
- 原始來源：[版本頁](https://proceedings.mlr.press/v139/nichol21a.html)；[本機 PDF](https://proceedings.mlr.press/v139/nichol21a.html)。
- 取得及整理日期：2026-11-23。
- 狀態：已 ingest 與入門主題相關的內容；使用者閱讀待完成。
- 閱讀範圍：PDF 第 1、3–4、6、8 頁；第 4 頁參數化、混合目標與排程圖已看原頁圖像。未逐表摘錄數值或重新訓練。

## 入門摘要

改良包含排程、訓練目標、變異數和取樣設定；不宜簡化成把 DDPM 換成 DDIM。

## 可回查主張

| 主張 ID | 作者內容的白話整理與 AI 界線 | 原文定位 |
|---|---|---|
| S03-C01 | 以特定變異數參數化與混合訓練目標學習反向過程變異數，改進原先固定變異數的設定。 | 第 3.1 節式 (15)、(16)；PDF 第 3–4 頁。 |
| S03-C02 | 提出 cosine 雜訊排程，調整訊號隨時間被破壞的方式；與原先線性 β 排程不同。 | 第 3.2 節式 (17)、Figure 3、5；PDF 第 4 頁。 |
| S03-C03 | 作者測試使用少於訓練時間步數的取樣流程；學習變異數的模型在其實驗條件下能以較少步數維持較佳生成品質。 | 第 4 節、Figure 8；PDF 第 6 頁。 |
| S03-C04 | 其 Figure 8 中 DDIM 與作者取樣法的比較隨步數與訓練進度改變，不能整理成所有情況下單一方法都最好。 | 第 4 節、Figure 8；PDF 第 6 頁。後半為 AI 的比較界線。 |

## 限制與待確認

未重現論文模型，也不據此推論超音波、FPGA 或臨床結果。個人心得待補。

## 連到知識網絡
- [雜訊排程](../concepts/noise-schedule.md)
- [反向取樣](../concepts/reverse-sampling.md)

[返回 Wiki 目錄](../index.md)
