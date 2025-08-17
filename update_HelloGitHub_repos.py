import requests
from bs4 import BeautifulSoup
import re

README_FILE = "README.md"
MAX_REPOS = 6  # 展示前几个热门仓库
URL = "https://hellogithub.com/"  # HelloGitHub 首页热门仓库

def get_hellogithub_top_repos(max_repos=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 找到热门仓库列表，选择器可能随网站结构变化需要调整
    repo_elements = soup.select("a.repo-title")  # 根据页面 HTML 调整
    top_repos = []

    for elem in repo_elements[:max_repos]:
        name = elem.text.strip()
        link = elem["href"]
        if not link.startswith("http"):
            link = "https://hellogithub.com" + link
        top_repos.append({"name": name, "link": link})

    return top_repos

def generate_markdown(repos):
    md = ""
    for repo in repos:
        name = repo["name"]
        link = repo["link"]
        # 使用 ReadMe Repo Card 或普通 Markdown 链接
        md += f"[{name}]({link})  \n"
    return md

def update_readme(markdown):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    # 替换占位符
    content = re.sub(r"<!--POPULAR_REPOS-->.*?<!--POPULAR_REPOS_END-->", f"<!--POPULAR_REPOS-->\n{markdown}<!--POPULAR_REPOS_END-->", content, flags=re.DOTALL)
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    top_repos = get_hellogithub_top_repos(MAX_REPOS)
    md = generate_markdown(top_repos)
    update_readme(md)
    print("README.md 已更新 HelloGitHub 热门仓库！")

if __name__ == "__main__":
    main()
