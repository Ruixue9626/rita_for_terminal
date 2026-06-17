# ✨ Rita - 你的終端機 AI 小助手 ✨

Rita 是一個基於 Google Gemini 3.1 模型的命令列工具，旨在幫助 Linux 使用者解釋指令、修正錯誤，並透過自然語言生成指令。她不只實用，還帶有一點點個性喔！ (｡･ω･｡)

## 🌟 主要功能

- **自動修正**：當你上一個指令失敗時，直接輸入 `rita`，她會幫你分析錯誤並提供修正建議。
- **指令解釋**：使用 `rita ask` 詢問指令的用途與詳細說明。
- **自然語言轉指令**：直接告訴 Rita 你想做什麼（例如：`rita 幫我找出大於 100MB 的檔案`），她會給你建議的指令。
- **Shell 整合**：支援 Bash 與 Zsh，自動同步歷史紀錄以便精準分析。

## 🚀 安裝步驟

1. **下載並執行安裝腳本**：
   在專案目錄下執行以下指令：
   ```bash
   chmod +x install.sh
   sudo ./install.sh
   ```

2. **設定 API Key**：
   前往 Google AI Studio 取得 API Key，然後執行：
   ```bash
   rita api
   ```

3. **設定環境同步**：
   為了讓 Rita 能讀取到最新的指令紀錄，請執行：
   ```bash
   rita setup
   ```
   執行完後，請重新啟動終端機或執行 `source ~/.bashrc` (或 `~/.zshrc`)。

## 📖 使用說明

### 1. 修正上一個出錯的指令
如果你剛才輸入的指令報錯了，直接輸入：
```bash
rita
```
Rita 會分析錯誤並問你是否要執行修正後的指令。

### 2. 詢問指令用法
想知道某個指令怎麼用？
```bash
rita ask tar
```
或是直接詢問剛才執行失敗的指令：
```bash
rita ask
```

### 3. 用講的也能通
直接描述你的需求：
```bash
rita 幫我把目前資料夾所有的 jpg 轉成 png
```

## 🛠 需求環境
- Python 3.6+
- 網路連線 (用於呼叫 Gemini API)
- Ubuntu / Linux 環境 (部分功能針對 Ubuntu 優化)# rita_for_terminal
