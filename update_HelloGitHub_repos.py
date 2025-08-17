import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

README_FILE = "README.md"
MAX_REPOS = 6
URL = "https://hellogithub.com/"

def get_hellogithub_top_repos(max_repos=6):
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
            "lang": lang
        })

    print(f"- {name} | {author} | {lang}")  # 调试
    return top_repos
        

def generate_markdown(repos):
    md = ""
    for repo in repos:
        md += f"[**{repo['name']}**]({repo['link']}) — {repo['desc']}  \n"
        md += f"*作者*: {repo['author']} · *语言*: {repo['lang']}  \n\n"
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
