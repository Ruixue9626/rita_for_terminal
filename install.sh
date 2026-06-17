#!/bin/bash

echo "等、等等啦！Rita 正在努力搬家中... ///"

# 1. 檢查檔案是否存在
if [ ! -f "rita.py" ]; then
    echo "欸欸！？Ruixue 醬，我找不到 rita.py 耶... 請確認妳在正確的資料夾喔！"
    exit 1
fi

# 2. 把檔案複製到系統路徑 /usr/local/bin，並改名成 rita
# 這樣系統就會把它當作一個正式的指令了！
echo "正在把我搬進系統執行路徑... (這需要 sudo 權限喔 >///<)"
sudo cp rita.py /usr/local/bin/rita

# 3. 給予執行權限
sudo chmod +x /usr/local/bin/rita

echo "太好啦！搬家完成！"
echo "Ruixue 醬，現在妳可以隨時在終端機輸入 \`rita\` 呼喚我了喔！"
echo "別忘了第一次使用要先輸入 \`rita api\` 讓我有動力工作喔！///"