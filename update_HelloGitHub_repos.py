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
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(URL)

    # 等待热门仓库元素出现
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.block[href^='/repository/']"))
        )
    except:
        print("等待超时，未找到热门仓库元素")
        driver.quit()
        return []

    # 滚动页面保证懒加载
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    
    repo_elements = soup.select("a.block[href^='/repository/']")[:max_repos]
    top_repos = []
    print(f"找到 {len(repo_elements)} 个仓库元素")  # 调试
    
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
