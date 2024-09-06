import requests
import json
import os
from datetime import datetime
# 获取当前时间
def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
    
# 获取下载链接
def getsource(name,url, img_url, program_url,number):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            releases = response.json()
            id = releases["id"]
            assets = releases["assets"]
            download_urls = []
            for a in number:
                asset=assets[a]
                download_urls.append({"name": asset["name"], "download_url": asset["browser_download_url"]})
            data={name:{"id": id, "name": name, "program_url": program_url, "img_url": img_url, "download_urls": download_urls}}
            return data
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

# 比较版本
def version_compare(name,data):
    if os.path.exists("config/id.json"):
        aa=read_json("config/id.json")
        if aa["name"]==data[name]["id"]:
            return False
        else:
            return True
    else:
        return True
# 读取json文件
def read_json(file_path, encoding='utf-8'):
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

# 写入json文件
def save_json(data, encoding='utf-8'):
    app_path = os.path.join('config', 'id.json')
    try:
        with open(app_path, 'w', encoding=encoding) as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"File '{app_path}' written successfully.")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
# 生成消息列表
def generate_message(data,name):
     try:
            bg=""
            data=data[name]
            for url in data["download_urls"]:
                bg += f"{url['name']}：[下载链接]({url['download_url']}) [代理1](https://mirror.ghproxy.com/{url['download_url']}) [代理2](https://slink.ltd/{url['download_url']})\n"
            name=data["name"]
            id=data["id"]
          
            program_url=data["program_url"]
            x=f"**{name}**\n\n**版本 ID: {id}**\n\n[{name} 开源地址]({program_url})\n\n**下载链接:**\n{bg}\n\n**发布时间: {get_time()}**"
            return x
                     
     except FileNotFoundError:
        return None
     except IOError as e:
        print(f"An error occurred while reading the template file: {e}")
        return None
# 发送消息
def send_message(photo_url,caption):
    bot_token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('TELEGRAM_ID')
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'
    data = {
        'chat_id': chat_id,
        'caption': caption,
        'parse_mode': 'Markdown'
    }
    files = {
        'photo': requests.get(photo_url).content
    }

    response = requests.post(url, data=data, files=files)
    print( response.status_code)

def main():
    file_path = 'config/download.json'
    data=read_json(file_path)
    all={}
    for item in data:
        url=item["url"]
        img_url=item["img_url"]
        program_url=item["program_url"]
        name=item["name"]
        number=item["number"]
        source=getsource(name,url,img_url,program_url,number)
        all.update({name:source[name]["id"]}) 
        if version_compare(name,source):
            message=generate_message(source,name)
            send_message(img_url,message)
    save_json(all)

if __name__ == '__main__':
    main()