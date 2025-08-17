import requests
from bs4 import BeautifulSoup
import re

README_FILE = "README.md"
MAX_REPOS = 6  # 展示前 5 个热门仓库
URL = "https://hellogithub.com/"

def get_hellogithub_top_repos(max_repos=6):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    repo_elements = soup.select("a.block[href^='/repository/']")[:max_repos]
    top_repos = []
    print(f"找到 {len(repo_elements)} 个仓库元素")  # 🔹调试
    for elem in repo_elements:
        link = "https://hellogithub.com" + elem["href"]
        # 名称在 <span class="font-semibold"> 标签内
        name_tag = elem.select_one("span.font-semibold")
        name = name_tag.text.strip() if name_tag else "Unknown"
        # 描述在 <span class="text-gray-600"> 内
        desc_tag = elem.select_one("span.text-gray-600")
        desc = desc_tag.text.strip() if desc_tag else ""
        # 作者
        author_tag = elem.select_one("div.truncate")
        author = author_tag.text.strip() if author_tag else ""
        # 编程语言
        lang_tag = elem.select_one("span.whitespace-nowrap")
        lang = lang_tag.text.strip() if lang_tag else ""
        print(f"- {name} | {author} | {lang}")  # 🔹调试
        
        top_repos.append({
            "name": name,
            "desc": desc,
            "link": link,
            "author": author,
            "lang": lang
        })
    return top_repos

def generate_markdown(repos):
    md = ""
    for repo in repos:
        md += f"[**{repo['name']}**]({repo['link']}) — {repo['desc']}  \n"
        md += f"*作者*: {repo['author']} · *语言*: {repo['lang']}  \n\n"
    return md

# def update_readme(markdown):
#     with open(README_FILE, "r", encoding="utf-8") as f:
#         content = f.read()
#     content = re.sub(
#         r"<!--POPULAR_REPOS-->.*?<!--POPULAR_REPOS_END-->",
#         f"<!--POPULAR_REPOS-->\n{markdown}<!--POPULAR_REPOS_END-->",
#         content,
#         flags=re.DOTALL
#     )
#     with open(README_FILE, "w", encoding="utf-8") as f:
#         f.write(content)
def update_readme(markdown):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"占位符起始位置: {start}, 结束位置: {end}")

    pattern = r"<!--POPULAR_REPOS-->(.|\s)*?<!--POPULAR_REPOS_END-->"
    replacement = f"<!--POPULAR_REPOS-->\n{markdown}<!--POPULAR_REPOS_END-->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)
    # 调试：写入后再读取并打印前 500 个字符
    with open(README_FILE, "r", encoding="utf-8") as f:
        check_content = f.read()
    print("写入后的内容预览（前500字符）：")
    print(check_content[:500])
# def main():
#     repos = get_hellogithub_top_repos(MAX_REPOS)
#     md = generate_markdown(repos)
#     update_readme(md)
#     print("README 已更新 HelloGitHub 最热仓库！") 

if __name__ == "__main__":
    repos = get_hellogithub_top_repos(MAX_REPOS)
    md = generate_markdown(repos)
    update_readme(md)
    print("README 已更新 HelloGitHub 热门仓库！")
