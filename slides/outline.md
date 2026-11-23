# 教學 HTML 簡報大綱：已確認

狀態：使用者於 2026-11-23 回覆「大綱可以，繼續製作簡報」，確認此 12 頁安排。

題名：從雜訊到影像：AI 怎麼學會畫圖？

讀者：有基本理工背景、未學過擴散模型的學生。預計 12 頁、約 10–15 分鐘；時間是教學規劃，尚未試講計時。

## 逐頁規劃

### 第 01 頁：今天要解開什麼問題？
- 教學目標：看到生成結果後，能說明訓練和生成各在做什麼。
- 內容／視覺安排：學習目標；以無條件影像生成作主線，條件生成另行標示。
- 來源主張：[S05-C01] [S01-C03]
- 證據卡：[s01-ddpm](../evidence/s01-ddpm.md)、[s05-understanding](../evidence/s05-understanding.md)

### 第 02 頁：生成模型在學什麼？
- 教學目標：由資料樣本學習模型，再產生新樣本。
- 內容／視覺安排：用資料分布的直覺圖；不展開機率推導。
- 來源主張：[S05-C01]
- 證據卡：[s05-understanding](../evidence/s05-understanding.md)

### 第 03 頁：先讓影像逐漸變成雜訊
- 教學目標：建立正向加雜訊的概念。
- 內容／視覺安排：同一張示意圖顯示不同雜訊程度；標示教學示意，不宣稱真實模型輸出。
- 來源主張：[S01-C01] [S03-C02]
- 證據卡：[s01-ddpm](../evidence/s01-ddpm.md)、[s03-improved-ddpm](../evidence/s03-improved-ddpm.md)

### 第 04 頁：訓練：猜加入了哪些雜訊
- 教學目標：分清楚訓練輸入、預測目標與參數更新。
- 內容／視覺安排：原圖、時間步、隨機雜訊、預測與誤差；用 DDPM 雜訊預測設定說明。
- 來源主張：[S01-C02] [S05-C02]
- 證據卡：[s01-ddpm](../evidence/s01-ddpm.md)、[s05-understanding](../evidence/s05-understanding.md)

### 第 05 頁：U-Net 在這裡做什麼？
- 教學目標：分清網路骨幹與整套生成流程。
- 內容／視覺安排：含雜訊表示＋時間步進入網路，輸出預測；不展開層數與張量尺寸。
- 來源主張：[S01-C04] [S04-C02]
- 證據卡：[s01-ddpm](../evidence/s01-ddpm.md)、[s04-latent-diffusion](../evidence/s04-latent-diffusion.md)

### 第 06 頁：生成：從隨機雜訊開始
- 教學目標：理解使用已訓練模型逐步取樣。
- 內容／視覺安排：強調原始 DDPM 中間步驟有隨機項；不是把某張原圖直接倒播回來。
- 來源主張：[S01-C03]
- 證據卡：[s01-ddpm](../evidence/s01-ddpm.md)

### 第 07 頁：訓練與生成，放在一起比較
- 教學目標：分辨是否用原圖與是否更新參數。
- 內容／視覺安排：兩欄表；註明無條件取樣情境，其他任務可能需要影像條件。
- 來源主張：[S01-C02] [S01-C03] [S05-C03]
- 證據卡：[s01-ddpm](../evidence/s01-ddpm.md)、[s05-understanding](../evidence/s05-understanding.md)

### 第 08 頁：為什麼生成需要時間？
- 教學目標：理解重複網路計算的成本與步數設定。
- 內容／視覺安排：原 DDPM 的 1000 步是本文設定；取樣步數可另設計。
- 來源主張：[S01-C05] [S02-C02]
- 證據卡：[s01-ddpm](../evidence/s01-ddpm.md)、[s02-ddim](../evidence/s02-ddim.md)

### 第 09 頁：兩種改良：取樣與訓練設定
- 教學目標：知道 DDIM 與 Improved DDPM 各改什麼。
- 內容／視覺安排：兩欄各三個短重點；DDIM 的確定性保留 η=0 條件，不列普遍速度倍數。
- 來源主張：[S02-C01] [S02-C02] [S02-C03] [S03-C01] [S03-C02] [S03-C03]
- 證據卡：[s02-ddim](../evidence/s02-ddim.md)、[s03-improved-ddpm](../evidence/s03-improved-ddpm.md)

### 第 10 頁：另一個方向：在潛在空間生成
- 教學目標：理解編碼表示、擴散與解碼的角色。
- 內容／視覺安排：區分訓練原圖編碼與生成新潛在樣本解碼；補一句壓縮可能影響精細準確性。
- 來源主張：[S04-C01] [S04-C02] [S04-C04] [S04-C05]
- 證據卡：[s04-latent-diffusion](../evidence/s04-latent-diffusion.md)

### 第 11 頁：你能分清楚了嗎？
- 教學目標：檢查學習目標。
- 內容／視覺安排：三個概念辨識：訓練／生成、DDIM 是否必然重訓、壓縮是否完全無損；屬教學自評，不假裝已對學生施測。
- 來源主張：[S01-C02] [S01-C03] [S02-C01] [S04-C04]
- 證據卡：[s01-ddpm](../evidence/s01-ddpm.md)、[s02-ddim](../evidence/s02-ddim.md)、[s04-latent-diffusion](../evidence/s04-latent-diffusion.md)

### 第 12 頁：重點回顧與五份來源
- 教學目標：回想三個改良軸並知道如何回查。
- 內容／視覺安排：簡短回顧；五份來源與 Wiki 入口。
- 來源主張：[S01-C02] [S02-C02] [S03-C01] [S04-C01] [S05-C01]
- 證據卡：[s01-ddpm](../evidence/s01-ddpm.md)、[s02-ddim](../evidence/s02-ddim.md)、[s03-improved-ddpm](../evidence/s03-improved-ddpm.md)、[s04-latent-diffusion](../evidence/s04-latent-diffusion.md)、[s05-understanding](../evidence/s05-understanding.md)

## 確認項目

頁數、順序、難度與範圍是否合適；大綱確認後才開始寫正式逐頁稿。正文以圖解為主，不展開 ELBO、ODE、score 推導或硬體實驗。

## 來源覆蓋方式

五份來源均有教學頁的主張對應，而不只列在最後一頁；檢查輸出見 [大綱覆蓋檢查](../reports/outline-coverage.txt)。
