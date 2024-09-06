import requests
import json
import os

def getsource(url, img_url, program_url, name):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            releases = response.json()
            id = releases["id"]
            assets = releases["assets"]
            download_urls = []
            for asset in assets:
                download_urls.append({"name": asset["name"], "download_url": asset["browser_download_url"]})
            data=({"id": id, "name": name, "program_url": program_url, "img_url": img_url, "download_urls": download_urls})
            return data
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


def read_json_file(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        return None


def read_template(template_path):

    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template = file.read()
            return template
    except FileNotFoundError:
        print(f"Template file '{template_path}' not found.")
        return None
    except IOError as e:
        print(f"An error occurred while reading the template file: {e}")
        return None
def generate_download_table(download_urls):
    table_rows = []
    for url in download_urls:
        row = f"| {url['name']} | [{url['download_url']}]({url['download_url']}) |\n"
        table_rows.append(row)
    return ''.join(table_rows)

# 将数据填入模板
def fill_template(template, data):
    filled_template = template.format(
        name=data["name"],
        id=data["id"],
        program_url=data["program_url"],
        img_url=data["img_url"],
        download_table=generate_download_table(data["download_urls"])
    )
    return filled_template
# 保存 Markdown 文件
def save_markdown_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
            print(f"Markdown file '{file_path}' written successfully.")
    except IOError as e:
        print(f"An error occurred while writing the Markdown file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


file_path = 'config/download.json'
data = read_json_file(file_path)
all=[]
if data is not None:
    for item in data:
       all.append(getsource(item["url"], item["img_url"], item["program_url"], item["name"]))

app_path = os.path.join('config', 'all.json')
 
try:
    with open(app_path, 'w', encoding='utf-8') as file:
        json.dump(all, file, ensure_ascii=False, indent=4)
    print(f"File '{app_path}' written successfully.")
except IOError as e:
    print(f"An error occurred while writing to the file: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
for item in all:
        template = read_template('config/templates.md')

        # 填充模板
        filled_template = fill_template(template, item)

        # 保存 Markdown 文件
        md_path = os.path.join('message', f'{item['name']}.md')
        save_markdown_file(md_path, filled_template)
