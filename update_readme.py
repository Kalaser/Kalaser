"""
update_readme.py

作者: Kalaser
描述: 主页获取每日一言，更新主页
日期: 2025-08-17
"""

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

# 获取今日图片并保存
def get_image():
    """获取今日图片并保存到当前分支目录"""
    url = "https://60s.viki.moe/v2/bing?encoding=image"
    filename = "daily.jpg"  # 保存的文件名
    
    try:
        # 下载图片
        with urllib.request.urlopen(url, timeout=10) as res:
            image_url = res.geturl()
            with urllib.request.urlopen(image_url, timeout=10) as img_res:
                with open(filename, "wb") as f:
                    f.write(img_res.read())
            print(f"✅ 图片已保存到 {filename}")
        
        # 自动添加到 git 暂存区（可选）
        subprocess.run(["git", "add", filename], check=True)
        subprocess.run(["git", "commit", "-m", "更新每日图片"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ 已提交最新图片到本地分支")
        
        return os.path.abspath(filename)

    except Exception as e:
        print(f"❌ 获取或保存图片失败: {e}")
        return None

def main():
    image = get_image()
    # 读取 README 文件内容
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # 获取当前日期和每日一言
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    quote = get_quote()
    # image = get_image()

    # 更新 README 中的日期和一言内容
    content = re.sub(r"<!--DATE-->.*", f"<!--DATE-->{today}", content)
    content = re.sub(r"<!--QUOTE-->.*", f"<!--QUOTE-->{quote}", content)
    content = re.sub(r"<!--IMAGE_URL-->.*", f"<!--IMAGE_URL-->{image}", content)
    # 将更新后的内容写回 README 文件
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()
