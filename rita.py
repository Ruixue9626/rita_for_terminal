#!/usr/bin/env python3
import sys
import os
import json
import urllib.request
import urllib.error
import subprocess
import time

CONFIG_FILE = os.path.expanduser("~/.rita_config")
# 預設使用 Google AI Studio 的 API 格式，並指定你要求的 Gemma 3 27B 模型 ///
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key="

def load_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()
    return None

def save_api_key(key):
    with open(CONFIG_FILE, "w") as f:
        f.write(key)
    print("成功記住 API Key 了喔！>///<")

def get_last_command_with_error():
    last_cmd = ""
    history_files = [
        os.environ.get("HISTFILE"),
        os.path.expanduser("~/.bash_history"),
        os.path.expanduser("~/.zsh_history"),
        os.path.expanduser("~/.history")
    ]

    try:
        for hist_path in filter(None, history_files):
            if os.path.exists(hist_path):
                with open(hist_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                
                for line in reversed(lines):
                    line = line.strip()
                    if not line: continue

                    # 處理 Zsh 格式 ": 1700000000:0;command"
                    if line.startswith(":"):
                        parts = line.split(";", 1)
                        if len(parts) == 2:
                            line = parts[1].strip()
                    
                    # 過濾掉 rita 相關指令
                    if line and not any(line.startswith(c) for c in ["rita", "history", "fc"]):
                        last_cmd = line
                        break
                if last_cmd: break
    except Exception as e:
        print(f"嗚... 讀取歷史紀錄失敗了：{e} ///")
        return "", ""
    
    # 嘗試執行這個指令，抓取錯誤訊息
    error_msg = ""
    if last_cmd:
        try:
            result = subprocess.run(last_cmd, shell=True, capture_output=True, text=True, timeout=2)
            if result.returncode != 0:
                # 優先顯示 stderr，如果沒有就顯示 stdout
                error_msg = result.stderr.strip() if result.stderr.strip() else result.stdout.strip()
                if not error_msg:
                    error_msg = f"Exit code: {result.returncode}"
        except subprocess.TimeoutExpired:
            error_msg = "指令執行超時"
        except Exception as e:
            error_msg = str(e)
    
    return last_cmd, error_msg

def ask_gemma(prompt, api_key):
    print("✨ 生成中... ///")
    url = API_URL + api_key
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            return res['candidates'][0]['content']['parts'][0]['text'].strip()
    except urllib.error.HTTPError as e:
        return f"欸欸！？API 好像出錯了... (HTTP {e.code}) ///"
    except Exception as e:
        return f"嗚... 發生未知錯誤：{e} >///<"

def setup_shell_integration():
    """自動偵測 Shell 並加入歷史紀錄同步設定"""
    shell_path = os.environ.get("SHELL", "")
    home = os.path.expanduser("~")
    
    if "zsh" in shell_path:
        rc_file = os.path.join(home, ".zshrc")
        line = 'setopt INC_APPEND_HISTORY'
    else:
        # 預設為 Bash
        rc_file = os.path.join(home, ".bashrc")
        line = 'export PROMPT_COMMAND="history -a;$PROMPT_COMMAND"'

    if not os.path.exists(rc_file):
        print(f"找不到設定檔 {rc_file} ... ///")
        return

    try:
        with open(rc_file, "r") as f:
            content = f.read()
        
        if line in content:
            print(f"妳的 {rc_file} 已經設定過同步功能囉！(｡･ω･｡) ///")
        else:
            with open(rc_file, "a") as f:
                f.write(f"\n# Rita history sync\n{line}\n")
            print(f"成功將設定寫入 {rc_file} 了！✨")
            print(f"請重新開啟終端機，或執行 `source {rc_file}` 來套用設定喔！>///<")
    except Exception as e:
        print(f"設定失敗了... 錯誤原因：{e} ///")

def main():
    args = sys.argv[1:]

    # 設定 API
    if len(args) == 1 and args[0] == "api":
        key = input("請輸入 Gemma 3 API Key：")
        save_api_key(key)
        return

    # 設定環境同步
    if len(args) == 1 and args[0] == "setup":
        setup_shell_integration()
        return

    api_key = load_api_key()
    if not api_key:
        print("欸、那個... 你還沒有設定 API Key 喔！請先輸入 `rita api` 來設定 >///<")
        return

    # rita ask 指令
    if len(args) >= 1 and args[0] == "ask":
        if len(args) > 1:
            cmd = " ".join(args[1:])
            error_msg = ""
        else:
            cmd, error_msg = get_last_command_with_error()
            if not cmd:
                print("找、找不到上一個指令啦... ///")
                return
        
        print(f"正在幫你詢問「{cmd}」的用法... 請等我一下喔 ///")
        if error_msg:
            prompt = f"請用繁體中文詳細但好懂地解釋這個 Linux 指令的用法與功能：{cmd}\n錯誤訊息：{error_msg}"
        else:
            prompt = f"請用繁體中文詳細但好懂地解釋這個 Linux 指令的用法與功能：{cmd}"
        answer = ask_gemma(prompt, api_key)
        print("\n" + answer + "\n")
        return

    # rita (預設：修正上一個指令)
    if len(args) == 0:
        cmd, error_msg = get_last_command_with_error()
        if not cmd:
            print("欸！？歷史紀錄空空的，不知道要修正什麼... >///<")
            return
            
        print(f"正在檢查上一個指令「{cmd}」... ///")
        if error_msg:
            prompt = f"用戶剛才在 Ubuntu 終端機輸入的指令失敗：{cmd}\n錯誤訊息：{error_msg}\n請直接回覆修正後「正確的完整指令」，不要加任何解釋或 markdown 標籤，只要一行指令就好。"
        else:
            prompt = f"用戶剛才在 Ubuntu 終端機輸入的指令失敗或有錯：{cmd}。請直接回覆修正後「正確的完整指令」，不要加任何解釋或 markdown 標籤，只要一行指令就好。"
        suggested_cmd = ask_gemma(prompt, api_key)
        
        # 移除可能被 AI 加上去的 markdown 區塊符號
        suggested_cmd = suggested_cmd.replace("```bash", "").replace("```", "").strip()
        
        print("\n💡 Rita 建議的修正指令：")
        print(f"  \033[1;32m{suggested_cmd}\033[0m\n")  # 使用綠色粗體顯示建議指令

        # 模擬按鈕功能：按下 Enter 直接執行
        confirm = input("👉 按下 [Enter] 立即執行指令，或輸入 [n] 取消... ")
        if confirm.lower() != 'n':
            print(f"🚀 執行中: {suggested_cmd}")
            os.system(suggested_cmd)
        else:
            print("👌 已取消執行。")
        return

    # rita [描述想做的事]
    query = " ".join(args)
    print(f"正在思考如何幫你「{query}」... ///")
    prompt = f"用戶想要在 Ubuntu 終端機執行此任務：{query}\n請直接回覆對應的「正確完整指令」，不要加任何解釋或 markdown 標籤，只要一行指令就好。"
    suggested_cmd = ask_gemma(prompt, api_key)

    # 移除可能被 AI 加上去的 markdown 區塊符號
    suggested_cmd = suggested_cmd.replace("```bash", "").replace("```", "").strip()

    print("\n💡 Rita 建議的指令：")
    print(f"  \033[1;32m{suggested_cmd}\033[0m\n")

    confirm = input("👉 按下 [Enter] 立即執行指令，或輸入 [n] 取消... ")
    if confirm.lower() != 'n':
        print(f"🚀 執行中: {suggested_cmd}")
        os.system(suggested_cmd)
    else:
        print("👌 已取消執行。")

if __name__ == "__main__":
    main()