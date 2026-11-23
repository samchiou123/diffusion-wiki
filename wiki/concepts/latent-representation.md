# 潛在表示（Latent representation）

## 白話概念

潛在擴散以學得的編碼器／解碼器建立較低維度表示，在這個空間進行擴散並將生成結果解碼回影像。[S04-C01] [S04-C02]

## 與其他概念的關係

「改在哪個空間生成」與「改怎麼取樣」是不同設計軸：LDM 的部分實驗使用 DDIM。[S04-C05] 原圖編碼是訓練／重建流程的一部分，不能把它畫成每次無條件生成都必須輸入原圖。這是依 [訓練與生成](../comparisons/training-vs-generation.md) 所作的 AI 教學整理。

## 限制

壓縮重建可能影響精細像素準確性，不能宣稱完全無損。[S04-C04]

依據：[Latent Diffusion](../sources/latent-diffusion.md)。延伸：[條件生成](conditional-generation.md)、[U-Net](unet-role.md)。

[返回目錄](../index.md)
