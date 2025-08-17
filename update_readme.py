import datetime
import re
import urllib.request
import json

README_FILE = "README.md"

# 获取每日一言
def get_quote():
    try:
        url = "https://60s.viki.moe/v2/hitokoto/?encoding=json"
        with urllib.request.urlopen(url, timeout=10) as res:
            data = json.load(res)
            return data.get("data", {}).get("hitokoto", "Keep coding, keep growing!")
    except Exception as e:
        print(f"Error fetching quote: {e}")
        return "Stay motivated!"

def main():
    # 读取 README 文件内容
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 获取当前日期和每日一言
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    quote = get_quote()

    # 更新 README 中的日期和一言内容
    content = re.sub(r"<!--DATE-->.*", f"<!--DATE-->{today}", content)
    content = re.sub(r"<!--QUOTE-->.*", f"<!--QUOTE-->{quote}", content)

    # 将更新后的内容写回 README 文件
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()
