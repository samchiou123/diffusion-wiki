# 擴散模型入門：LLM Wiki 與教學簡報

以有基本理工背景、尚未學過擴散模型的大學生／研究生為對象，從加雜訊、訓練到生成建立入門概念，再比較 DDIM、Improved DDPM 與潛在擴散。

## 成果入口

- **HTML 教學簡報**：GitHub Pages 部署後，使用該網站的根網址閱讀。本機可直接開啟 [index.html](index.html)。GitHub 檔案頁只顯示 HTML 原始碼。
- **LLM Wiki**：[wiki/index.md](wiki/index.md)，包含五份來源、八個概念、跨篇比較與查詢成果。
- **Loop／Graph**：[工作流程](workflows/wiki-to-slides.md)。
- **實際執行與反思**：[第三階段紀錄](reports/deck-stage3.md)、[公開包檢查](reports/public-package-check.txt)。
- **來源清單**：[raw/source-catalog.json](raw/source-catalog.json)，包含固定版本與原始論文連結。
- **逐頁稿**：[slides/drafts.md](slides/drafts.md)。

## Wiki 如何運作

參考使用者提供的 Karpathy LLM Wiki 構想：原始來源與清單、可累積的 Wiki、AGENTS.md 規則文件形成三層架構。Ingest 逐篇讀取並將主張整合到概念頁，Query 查詢後將可重用答案回存，Lint 檢查結構與來源。這是 AI 配合檔案交接的工作流程，沒有宣稱已建立全自動排程程式。

來源取得 → 逐篇 ingest → Wiki 就緒關卡 → 查詢及證據卡 → 大綱確認 → 逐頁稿與內容核對 → HTML 與畫面檢查。來源不足退回 ingest；內容問題退回證據或稿件；排版問題只重跑 HTML。每個修正節點最多三輪。

## 進度與檢查界線

五份不同資料的主題相關 ingest 與 12 頁簡報已完成。使用者已下載閱讀。結構、文字一致性、JavaScript 語法、翻頁索引純函式及靜態列印檢查已有紀錄；逐項瀏覽器點擊、焦點與手機視窗結果尚未記錄，不能視為通過。

依使用者選擇，本次跳過獨立新對話審查；紀錄為「未執行」，不列為發布阻擋項目。保留生成者來源自查與實際製作紀錄。歷史報告保留當時的待辦狀態，最新決定以本 README 與 wiki/log.md 末筆紀錄為準。

此包尚未替使用者部署網站。上傳 GitHub 後，在 Settings → Pages 設定 Deploy from a branch、main、/(root)，再依 GitHub 顯示的網站網址驗證。

## 公開包與原始資料

這是適合上傳 GitHub 的公開版，沒有附上五份論文 PDF。來源清單仍保留原文網址、固定版本、閱讀範圍與雜湊；完整本機資料包才保留原始 PDF。公開包的檢查使用：

```bash
python3 scripts/lint_wiki.py --require-five --metadata-only
python3 scripts/check_outline.py
python3 scripts/check_deck.py
node --check slides/deck-script.js
node scripts/test_navigation.cjs
```

metadata-only 模式只檢查來源紀錄、主張、目錄與內部連結，不驗證原文 PDF 是否存在或雜湊是否相符。完整包使用不帶該旗標的嚴格檢查。公開包若要重新核對原文，先依來源清單取得相同版本並恢復 raw 路徑。

HTML 含內嵌樣式、程式與 SVG，翻頁、自評與來源可展開；外部論文連結需要網路。修改內容須先修逐頁稿與來源核對，不在 HTML 排版時偷改已凍結的文字。

## AI 使用說明

ChatGPT 協助需求討論、來源整理、Wiki、比較、逐頁稿、流程圖、HTML 與檢查程式。教學像素圖為示意，未重現模型實驗；沒有代寫個人心得、捏造獨立審查或學習成效。最終繳交說明及實際觀察由本人核對。
