import requests
from bs4 import BeautifulSoup
import re

README_FILE = "README.md"
MAX_REPOS = 5  # 展示前 5 个热门仓库
URL = "https://hellogithub.com/"

def get_hellogithub_top_repos(max_repos=5):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 根据 HelloGitHub HTML 结构抓取热门仓库链接
    repo_elements = soup.select("a[href^='/repository/']")
    top_repos = []

    for elem in repo_elements[:max_repos]:
        repo_path = elem["href"]
        repo_url = "https://hellogithub.com" + repo_path
        repo_name = repo_path.split("/")[-1]
        top_repos.append({"name": repo_name, "link": repo_url})

    return top_repos

def generate_markdown(repos):
    md = ""
    for repo in repos:
        # 使用简单 Markdown 链接，也可以改成 ReadMe Repo Card 样式
        md += f"[{repo['name']}]({repo['link']})  \n"
    return md

def update_readme(markdown):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(
        r"<!--POPULAR_REPOS-->.*?<!--POPULAR_REPOS_END-->",
        f"<!--POPULAR_REPOS-->\n{markdown}<!--POPULAR_REPOS_END-->",
        content,
        flags=re.DOTALL,
    )
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    repos = get_hellogithub_top_repos(MAX_REPOS)
    md = generate_markdown(repos)
    update_readme(md)
    print("README 已更新 HelloGitHub 最热仓库！") 

if __name__ == "__main__":
    main()
