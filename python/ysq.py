'''
Author: bgcode
Date: 2025-03-28 07:14:22
LastEditTime: 2025-04-12 07:35:16
LastEditors: bgcode
Description: 描述
FilePath: /Autoaction/python/ysq.py
本项目采用GPL 许可证，欢迎任何人使用、修改和分发。
'''
import requests
import re
import os
from urllib.parse import quote


def remove_duplicate_cookies(cookie_str):
    cookie_dict = {}
    cookie_pairs = cookie_str.split(';')
    for pair in cookie_pairs:
        pair = pair.strip()
        if '=' in pair:
            key, value = pair.split('=', 1)
            cookie_dict[key] = value
    new_cookie_str = '; '.join([f"{key}={value}" for key, value in cookie_dict.items()])
    return new_cookie_str
def remove_cookie_keys(cookie_str, keys_to_remove):
    cookie_dict = {}
    cookie_pairs = cookie_str.split(';')
    for pair in cookie_pairs:
        pair = pair.strip()
        if '=' in pair:
            key, value = pair.split('=', 1)
            cookie_dict[key] = value
    for key in keys_to_remove:
        if key in cookie_dict:
            del cookie_dict[key]
    new_cookie_str = '; '.join([f"{key}={value}" for key, value in cookie_dict.items()])
    return new_cookie_str

class HttpClient:
    def __init__(self):
        self.host = ""
        self.cookie = ""
        self.loginhash = ""
        self.forhash = ""
        self.name = ""
        self.key = ""
        self.signhash = ""
        self.info=""
    def setenv(self,host,name,key):
        self.host = host
        self.name=quote(name)
        self.key=quote(key)
    def get_login_info(self):
        url = f'https://{self.host}/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Dest': 'empty',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Sec-Fetch-Mode': 'cors',
            'Host': self.host,
            'sec-ch-ua-platform': '"macOS"',
            'DNT': '1',
            'Referer': 'https://{self.host}/k_misign-sign.html',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        }   

        try:
            response = requests.get(url, headers=headers)
            # print(response.text)
            self.loginhash = re.search(r'loginhash=(.*?)"', response.text).group(1)
            self.forhash = re.search(r'formhash.*value="(.*?)"', response.text).group(1)
            for cookie in response.cookies:
                 self.cookie+=f"{cookie.name}={cookie.value};"
                 # cookies = response.headers.get("Set-Cookie", "")
            # print(self.cookie)
        except requests.RequestException as e:
            print(f"请求出错: {e}")    

    def login(self):
        url = f'https://{self.host}/member.php?mod=logging&action=login&loginsubmit=yes&loginhash={self.loginhash}&inajax=1'
        headers = {
            'Host': self.host,
            'Origin': 'https://{self.host}',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Referer': 'https://{self.host}/member.php?mod=logging&action=login',
            'Cookie': self.cookie,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = f'formhash={self.forhash}&referer=https%3A%2F%2Fysqbbs.com%2Fportal.php&username={self.name}&password={self.key}&questionid=0&answer='
        response = requests.post(url, headers=headers, data=data)
        for cookie in response.cookies:
                    self.cookie+=f"{cookie.name}={cookie.value};"
                    # cookies = response.headers.get("Set-Cookie", "")
        self.cookie= remove_duplicate_cookies(self.cookie)
        self.cookie= remove_cookie_keys(self.cookie, ['YPSa_2132_checkfollow', 'YPSa_2132_lip'])
        # print(self.cookie)
        
    def gethash(self):
        url = f"https://{self.host}/k_misign-sign.html"
        headers = {
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'Upgrade-Insecure-Requests': '1',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Host': self.host,
            'Cookie': self.cookie,
            'Referer': 'https://{self.host}/k_misign-sign.html',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        }
        response = requests.get(url, headers=headers)
        try:
            self.signhash = re.search(r'formhash=(.*?)"', response.text).group(1)
        except:
            self.signhash = ""
        # print( self.signhash)
        # print(response.text)
        
    def sign(self):
        if self.signhash=="":
            return False
        url=f'https://{self.host}/plugin.php?id=k_misign:sign&operation=qiandao&formhash={self.signhash}&format=empty&inajax=1&ajaxtarget='
        headers={
            'X-Requested-With' : 'XMLHttpRequest',
            'Sec-Fetch-Dest' : 'empty',
            'Connection' : 'keep-alive',
            'Accept-Encoding' : 'gzip, deflate, br, zstd',
            'sec-ch-ua' : '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile' : '?0',
            'Sec-Fetch-Site' : 'same-origin',
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Sec-Fetch-Mode' : 'cors',
            'Cookie' : self.cookie,
            'Host' : self.host,
            'sec-ch-ua-platform' : '"macOS"',
            'DNT' : '1',
            'Accept-Language' : 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Accept' : '*/*',
            'Referer' : 'https://{self.host}/k_misign-sign.html'
            }
        response = requests.get(url, headers=headers)
        # print(response.text) 

    def get_info(self):
        url=f'https://{self.host}/home.php?mod=spacecp&ac=credit'
        headers = {
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'Upgrade-Insecure-Requests': '1',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Host': self.host,
            'Cookie': self.cookie,
            'Referer': 'https://{self.host}/home.php?mod=spacecp&ac=credit&op=base',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        }
        response = requests.get(url, headers=headers)
        match = re.search(r'源币.*?>(\d+)', response.text)  # re.DOTALL 让 . 匹配换行符
        match1 = re.search(r'经验.*?>(\d+)', response.text)
        match2 = re.search(r'贡献.*?>(\d+)', response.text)
        match3 = re.search(r'积分.*?>(\d+)', response.text)
        # pattern = r'源币.*?>(\d+).*?经验.*?>(\d+).*?贡献.*?>(\d+).*?积分.*?>(\d+)'
        # match = re.search(pattern, response.text, re.DOTALL)  # re.DOTALL 让 . 匹配换行符
        # if match:
            # 提取四个捕获组的值（确保顺序正确）
        source_coin = match.group(1)
        experience = match1.group(1)
        contribution = match2.group(1)
        points = match3.group(1)
        self.info = f"源币:{source_coin}  经验:{experience}  贡献:{contribution}  积分:{points}"
        # else:
            # print("未找到匹配的内容")
        # print(self.info)
        return self.info
def main():
    client = HttpClient()
    host = "ysqbbs.com"
    account=os.environ.get('YSQ_ACCOUNT')
    password=os.environ.get('YSQ_PASSWORD')
    client.setenv(host,account,password)
    client.get_login_info()
    client.login()
    client.gethash()
    client.sign()
    info=  client.get_info()
    print(info)
    return info
# 运行示例
if __name__ == "__main__":
   main()
  
    