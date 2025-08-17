import datetime, requests, re

README_FILE = "README.md"

# 获取每日一句（你可以换成别的 API，例如一言、英文名言等）
def get_quote():
    try:
        res = requests.get("https://v1.hitokoto.cn/?encode=text")
        if res.status_code == 200:
            return res.text.strip()
    except:
        return "Keep coding, keep growing!"
    return "Stay motivated!"

def main():
    # 读取 README
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 更新日期和名言
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    quote = get_quote()

    content = re.sub(r"<!--DATE-->.*", f"<!--DATE-->{today}", content)
    content = re.sub(r"<!--QUOTE-->.*", f"<!--QUOTE-->{quote}", content)

    # 写回文件
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()
