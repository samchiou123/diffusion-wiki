# S05：Understanding Diffusion Models: A Unified Perspective

- 作者：Calvin Luo。
- 發表／版本：2022；arXiv v1 標示 8 月 25 日，文件封面另印 8 月 26 日。
- 原始來源：[版本頁](https://arxiv.org/abs/2208.11970)；[本機 PDF](https://arxiv.org/abs/2208.11970)。
- 取得及整理日期：2026-11-23。
- 狀態：已 ingest 與入門主題相關的內容；使用者閱讀待完成。
- 閱讀範圍：PDF 第 1、15、17、20–21 頁；第 17 頁三種參數化結語已看原頁圖像。只整理入門相關段落，未宣稱驗算全部推導。

## 入門摘要

本篇作為教學性綜整來源，用來界定名詞與適用範圍；不是把每個定義都當成本文新提出的模型。

## 可回查主張

| 主張 ID | 作者內容的白話整理與 AI 界線 | 原文定位 |
|---|---|---|
| S05-C01 | 生成模型以觀察到的樣本學習資料分布的模型，之後可從模型產生新樣本。 | Introduction: Generative Models；PDF 第 1 頁。 |
| S05-C02 | 在文中推導的 VDM 設定下，可將預測原圖、雜訊或 score 視為有關聯的參數化。 | Three Equivalent Interpretations；PDF 第 15–17 頁。教學不延伸成任意目標與權重訓練結果都相同。 |
| S05-C03 | 條件生成可加入 y，例如文字編碼或低解析度影像；無條件取樣不是所有影像生成任務的唯一輸入形式。 | Guidance、式 (162)；PDF 第 20 頁。後半為 AI 的教學整理。 |
| S05-C04 | Guidance 是進一步調整生成對條件的依循方式，文中說明與樣本多樣性的取捨。 | Guidance；PDF 第 21 頁。入門簡報不展開其完整公式。 |

## 限制與待確認

未重現論文模型，也不據此推論超音波、FPGA 或臨床結果。個人心得待補。

## 連到知識網絡
- [生成模型](../concepts/generative-models.md)
- [雜訊預測](../concepts/noise-prediction.md)
- [條件生成](../concepts/conditional-generation.md)

[返回 Wiki 目錄](../index.md)
