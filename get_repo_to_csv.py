import os
from dotenv import load_dotenv
import requests
import csv

load_dotenv()

# 你的 GitHub 個人 access token
TOKEN = os.getenv("TOKEN")
USERNAME = os.getenv("USERNAME")


def get_repositories(token):
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {token}"}
    repos = []
    page = 1

    while True:
        response = requests.get(url, headers=headers, params={"per_page": 100, "page": page, "visibility": "all"})
        if response.status_code != 200:
            raise Exception(f"GitHub API error: {response.status_code}, {response.text}")

        data = response.json()
        if not data:
            break

        for repo in data:
            repos.append({
                "name": repo["name"],
                "https_url": repo["clone_url"],
                "private": repo["private"]   # 顯示是否為私有 repo
            })
        page += 1

    return repos


def save_to_csv(repos, filename="repos.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "https_url","private"])
        writer.writeheader()
        writer.writerows(repos)
    print(f"[INFO] 已將 {len(repos)} 筆資料存到 {filename}")


if __name__ == "__main__":
    repositories = get_repositories(TOKEN)
    for repo in repositories:
        print(f"{repo['name']} → {repo['https_url']}")
    
    save_to_csv(repositories)
