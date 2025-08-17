"""
update_HelloGitHub_repos.py

作者: Kalaser
描述: 自动抓取 HelloGitHub 最热仓库，并生成带胶囊的 Markdown 到 README.md
日期: 2025-08-17
"""


import time
import re

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

README_FILE = "README.md"
MAX_REPOS = 8
URL = "https://hellogithub.com/"

def get_hellogithub_top_repos(max_repos=8):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL)
        page.wait_for_selector("a.block[href^='/repository/']", timeout=15000)
        html = page.content()
        browser.close()
    
    soup = BeautifulSoup(html, "html.parser")
    repo_elements = soup.select("a.block[href^='/repository/']")[:MAX_REPOS]
    top_repos = []
    if not repo_elements:
            print("未抓取到仓库元素")
            browser.close()
            return top_repos
    for elem in repo_elements:
        link = "https://hellogithub.com" + elem["href"]
        # 名称
        name_tag = elem.select_one("span.font-semibold")
        name = name_tag.text.strip() if name_tag else "Unknown"
        # 描述
        desc_tag = elem.select_one("span.text-gray-600")
        desc = desc_tag.text.strip() if desc_tag else ""
        # 作者
        author_tag = elem.select_one("div.truncate")
        author = author_tag.text.strip() if author_tag else ""
        # 语言
        lang_tag = elem.select_one("span.whitespace-nowrap")
        lang = lang_tag.text.strip() if lang_tag else ""
        top_repos.append({
            "name": name,
            "desc": desc,
            "link": link,
            "author": author,
            "lang": lang
        })
    # browser.close()
    print(f"- {name} | {author} | {lang}")  # 调试
    return top_repos
        

def generate_markdown(repos):
    for repo in repos:
        md += f"{i}. [{repo['name']}]({repo['link']})  \n"
        md += f'  <a href="{repo["link"]}" target="_blank" style="text-decoration:none;">\n'
        md += f'      <strong>{repo["name"]}</strong><br>\n'
        md += f'      作者: {repo["author"]}<br>\n'
        md += f'      语言: {repo["lang"]}<br>\n'
        md += f'  </a>\n\n'
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
