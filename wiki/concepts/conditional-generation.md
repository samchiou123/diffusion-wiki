# 條件生成（Conditional generation）

## 白話概念

除了隨機起始雜訊，模型還可以接收條件 y，例如文字編碼或低解析度影像，控制生成內容。[S05-C03] LDM 可用 cross-attention 引入文字等條件。[S04-C03]

## 不同輸入要分清楚

DDPM 原文 Algorithm 2 的無條件取樣不需要輸入原圖。[S01-C03] 這不代表影像到影像或超解析度任務也不需要條件影像。[S05-C03]

## 延伸界線

Guidance 涉及條件依循與多樣性取捨；本次入門簡報只介紹條件的作用，不展開其公式。[S05-C04]

依據：[DDPM](../sources/ddpm.md)、[Latent Diffusion](../sources/latent-diffusion.md)、[Luo 綜整](../sources/understanding-diffusion.md)。

[返回目錄](../index.md)
