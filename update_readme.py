#!/usr/bin/env python3
"""Refresh the GitHub profile README.

Fetches the public repositories owned by USERNAME from the GitHub REST API,
filters out forks and archived repositories, then rewrites the block between
PROJECTS_START and PROJECTS_END. Standard library only.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USERNAME = "Kalaser"
README = Path(__file__).resolve().parent / "README.md"
API_URL = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed"

MAX_PROJECTS = 12
INCLUDE_FORKS = False
INCLUDE_ARCHIVED = False

# Display order. Repositories not listed here are appended alphabetically.
FEATURED_ORDER = [
    "Uikit-Framework",
    "Sunny_OS",
    "cpp-navigator",
    "Mythreadpool",
    "Kalaser_agent",
    "kalaser_docmd",
    "Folder-Encryption-Tool",
    "C-Cpp--learning",
    "OASIS",
]

# English descriptions for repositories whose GitHub description is missing
# or written in another language. Repositories not listed here use the API
# description.
DESCRIPTIONS = {
    "Uikit-Framework": "UIKit-style widget and API layer over LVGL for embedded GUI development, with an optional C++ RAII wrapper.",
    "Sunny_OS": "Lightweight LVGL-based UI framework with a minimal shell, page router, and publish-subscribe data bus.",
    "cpp-navigator": "VS Code extension for fast C/C++ symbol indexing, navigation, and call-hierarchy exploration.",
    "Mythreadpool": "Thread pool implemented from scratch with queues, mutexes, read-write locks, and condition variables.",
    "Kalaser_agent": "Experimental TypeScript agent runtime and developer tooling.",
    "kalaser_docmd": "Engineering notes and technical guides, published as a static documentation site.",
    "Folder-Encryption-Tool": "Desktop GUI for encrypting and decrypting files inside a folder.",
    "C-Cpp--learning": "Personal C/C++ learning notes, exercises, and small projects.",
    "OASIS": "Personal sandbox for experiments and prototypes.",
}

# Optional label overrides when the GitHub language is missing or inaccurate.
STACK_OVERRIDES = {
    "kalaser_docmd": "Docs",
    "OASIS": "Sandbox",
}

PROJECTS_START = "<!-- PROJECTS:START -->"
PROJECTS_END = "<!-- PROJECTS:END -->"
UPDATED_START = "<!-- LAST_UPDATED:START -->"
UPDATED_END = "<!-- LAST_UPDATED:END -->"


def fetch_repos() -> list[dict]:
    headers = {
        "User-Agent": f"{USERNAME}-profile-readme",
        "Accept": "application/vnd.github+json",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    repos: list[dict] = []
    page = 1
    while True:
        request = urllib.request.Request(f"{API_URL}&page={page}", headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            batch = json.load(response)

        repos.extend(batch)
        if len(batch) < 100 or page >= 10:
            break
        page += 1

    return repos


def select_repos(repos: list[dict]) -> list[dict]:
    selected = []
    for repo in repos:
        if repo["name"].lower() == USERNAME.lower():
            continue
        if not INCLUDE_FORKS and repo.get("fork"):
            continue
        if not INCLUDE_ARCHIVED and repo.get("archived"):
            continue
        selected.append(repo)

    rank = {name: index for index, name in enumerate(FEATURED_ORDER)}
    selected.sort(key=lambda repo: (rank.get(repo["name"], len(rank)), repo["name"].lower()))
    return selected


def clean_text(value: str | None) -> str:
    text = re.sub(r"\s+", " ", value or "").strip()
    return text.replace("|", r"\|")


def render_projects(repos: list[dict]) -> str:
    lines = [
        "| Project | Stack | Description |",
        "| :--- | :--- | :--- |",
    ]
    for repo in repos[:MAX_PROJECTS]:
        name = repo["name"]
        description = clean_text(
            DESCRIPTIONS.get(name) or repo.get("description") or "No description provided."
        )
        stack = STACK_OVERRIDES.get(name) or repo.get("language") or "-"
        lines.append(f"| **[{name}]({repo['html_url']})** | `{stack}` | {description} |")
    return "\n".join(lines)


def replace_block(text: str, start: str, end: str, body: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if not pattern.search(text):
        raise SystemExit(f"Markers not found: {start} / {end}")
    replacement = f"{start}\n{body}\n{end}"
    return pattern.sub(lambda _match: replacement, text, count=1)


def main() -> int:
    try:
        repos = fetch_repos()
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"Failed to fetch repositories: {exc}", file=sys.stderr)
        return 1

    selected = select_repos(repos)
    if not selected:
        print("No repositories matched the filters; README left unchanged.", file=sys.stderr)
        return 1

    readme = README.read_text(encoding="utf-8")
    readme = replace_block(readme, PROJECTS_START, PROJECTS_END, render_projects(selected))

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    readme = replace_block(readme, UPDATED_START, UPDATED_END, timestamp)

    with README.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(readme)

    print(f"Updated {README.name} with {min(len(selected), MAX_PROJECTS)} repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())