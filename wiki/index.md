# 擴散模型入門 Wiki

目前已 ingest 5/5 份不同來源。只有閱讀過的內容進入主張表；原文未逐頁驗算的範圍各頁另列。

## 來源
- [S01：Denoising Diffusion Probabilistic Models](sources/ddpm.md)
- [S02：Denoising Diffusion Implicit Models](sources/ddim.md)
- [S03：Improved Denoising Diffusion Probabilistic Models](sources/improved-ddpm.md)
- [S04：High-Resolution Image Synthesis with Latent Diffusion Models](sources/latent-diffusion.md)
- [S05：Understanding Diffusion Models: A Unified Perspective](sources/understanding-diffusion.md)

## 概念
- [條件生成（Conditional generation）](concepts/conditional-generation.md)
- [正向擴散（Forward diffusion）](concepts/forward-diffusion.md)
- [生成模型（Generative models）](concepts/generative-models.md)
- [潛在表示（Latent representation）](concepts/latent-representation.md)
- [雜訊預測（Noise prediction）](concepts/noise-prediction.md)
- [雜訊排程（Noise schedule）](concepts/noise-schedule.md)
- [反向取樣（Reverse sampling）](concepts/reverse-sampling.md)
- [U-Net 在 DDPM 的角色](concepts/unet-role.md)

## 比較
- [方法比較：三個改良方向可以分開看](comparisons/diffusion-methods.md)
- [跨篇公式記號：同一個 α 不一定同義](comparisons/notation.md)
- [訓練與生成：先分清楚任務](comparisons/training-vs-generation.md)

## 查詢成果
- [為什麼訓練是預測雜訊，最後卻能產生影像？](questions/why-noise-prediction-generates-images.md)

## 維護與流程
- [操作紀錄](log.md)
- [來源清單](../raw/source-catalog.json)
- [工作流程](../workflows/wiki-to-slides.md)
- [已確認的教學大綱](../slides/outline.md)
- [正式逐頁稿](../slides/drafts.md)
- [教學 HTML 簡報](../index.html)
- [本輪檢查與反思](../reports/deck-stage3.md)
