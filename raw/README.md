# 原始來源與 ingest 範圍

五份 PDF 固定版本、取得日期、原始網址與 SHA-256 均列於 source-catalog.json。原始 PDF 不改寫；每次讀取、摘要與整合都以對應版本為準。

已 ingest 5/5 份不同來源的入門相關內容。這不表示逐頁驗算全部推導、逐表核對所有結果，或重現其模型。每篇來源摘要均明列實際閱讀範圍及視覺核對頁面。

| ID | 原始檔 | 本次閱讀範圍 |
|---|---|---|
| S01 | ddpm-v2.pdf | PDF 第 1–9、14–15 頁；第 4 頁算法視覺核對 |
| S02 | ddim-v4.pdf | PDF 第 1–2、4–6、9 頁；第 5 頁視覺核對 |
| S03 | improved-ddpm-v1.pdf | PDF 第 1、3–4、6、8 頁；第 4 頁視覺核對 |
| S04 | latent-diffusion-v2.pdf | PDF 第 1、3–5、9 頁；第 4 頁視覺核對 |
| S05 | understanding-diffusion-v1.pdf | PDF 第 1、15、17、20–21 頁；第 17 頁視覺核對 |

公開網頁呈現 Wiki 整理與來源連結；本公開包省略原始 PDF，保留 source-catalog.json 的版本、原文網址及原始雜湊；完整本機包才含 PDF。
