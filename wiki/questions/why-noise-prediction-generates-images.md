# 為什麼訓練是預測雜訊，最後卻能產生影像？

## 從 Wiki 回答

先看 [雜訊預測](../concepts/noise-prediction.md)：訓練用原圖建立含雜訊影像，讓網路預測加入的雜訊並更新參數。[S01-C02]

再看 [反向取樣](../concepts/reverse-sampling.md)：生成時不重新訓練，而是從隨機雜訊開始，多次呼叫已學好的預測網路，再依取樣更新式得到影像。[S01-C03]

因此「網路一次預測什麼」與「整套程序最後產生什麼」屬不同層次。這是依前述來源的 AI 教學整理。綜整文也說明雜訊預測只是相關參數化之一，不能說所有擴散模型都只能預測雜訊。[S05-C02]

## 限定情境

本題使用 DDPM 的簡化訓練與無條件生成。條件生成可能另有文字或影像輸入，見 [條件生成](../concepts/conditional-generation.md)。[S05-C03]

## 回存與來源

這份答案由 Wiki 目錄、概念與來源頁查詢後回存，示範 Karpathy 的 Query 累積方式。依據：[DDPM](../sources/ddpm.md)、[Luo](../sources/understanding-diffusion.md)。

[返回目錄](../index.md)
