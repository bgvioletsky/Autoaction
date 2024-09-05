import requests

def save_releases_to_md(repos):
    download_urls = []
    id=[]
    for repo in repos:
        url = f"https://api.github.com/repos/{repo}/releases/latest"
            # 发送GET请求获取仓库的发布信息
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            releases = response.json()
            id = releases["id"]
            assets=releases["assets"]
            for asset in assets:
                download_urls.append({"name":asset["name"],"download_url":asset["browser_download_url"]})
            print(id)
            print(download_urls)
            
# 示例使用
# owner = "octocat"  # 替换为实际的仓库拥有者
repos = ["Molunerfinn/PicGo", "alist-org/alist"]  # 替换为实际的仓库名称列表

save_releases_to_md(repos)
