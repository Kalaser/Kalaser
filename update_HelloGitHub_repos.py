"""
update_HelloGitHub_repos.py

作者: Kalaser
描述: 自动抓取 HelloGitHub 最热仓库，并生成带编号的 Markdown 到 README.md
日期: 2025-08-17
"""

import re
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

README_FILE = "README.md"
MAX_REPOS = 8
URL = "https://hellogithub.com/"

def get_hellogithub_top_repos(max_repos=8):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, timeout=60000, wait_until="networkidle")
        page.wait_for_selector("a.block[href^='/repository/']", timeout=15000)
        html = page.content()

    soup = BeautifulSoup(html, "html.parser")
    repo_elements = soup.select("a.block[href^='/repository/']")[:max_repos]
    print(f"找到 {len(repo_elements)} 个仓库元素")

    top_repos = []
    for elem in repo_elements:
        link = "https://hellogithub.com" + elem["href"]
        name_tag = elem.select_one("span.font-semibold")
        name = name_tag.text.strip() if name_tag else "Unknown"

        desc_tag = elem.select_one("span.text-gray-600")
        desc = desc_tag.text.strip() if desc_tag else ""

        author_tag = elem.select_one("div.truncate")
        author = author_tag.text.strip() if author_tag else ""

        lang_tag = elem.select_one("span.whitespace-nowrap")
        lang = lang_tag.text.strip() if lang_tag else ""

        top_repos.append({
            "name": name,
            "desc": desc,
            "link": link,
            "author": author,
            "lang": lang,
            "updated": ""  # 默认值
        })
        print(f"- {name} | {author} | {lang}")  # 调试
        top_repos ['updated'] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    return top_repos

def generate_markdown(repos):
    md = ""
    for i, repo in enumerate(repos, 1):
        md += f"{i}. [{repo['name']}]({repo['link']})  \n"
        md += f"   - 描述: {repo['desc']}  \n"
        md += f"   - 简介: `{repo['author']}`  \n"
        md += f"   - 语言: `{repo['lang']}`  \n"
        md += f"   - 更新时间: `{(repo.get('updated','未知'))}`  \n\n"
    return md

def update_readme(markdown):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"<!--POPULAR_REPOS-->(.|\s)*?<!--POPULAR_REPOS_END-->"
    replacement = f"<!--POPULAR_REPOS-->\n{markdown}<!--POPULAR_REPOS_END-->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README 已写入更新内容。")

if __name__ == "__main__":
    repos = get_hellogithub_top_repos(MAX_REPOS)
    if repos:
        md = generate_markdown(repos)
        update_readme(md)
    else:
        print("未抓取到仓库，不更新 README")
