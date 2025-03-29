'''
Author: bgcode
Date: 2025-03-28 07:14:22
LastEditTime: 2025-03-29 22:56:29
LastEditors: bgcode
Description: 描述
FilePath: /Autoaction/python/ysq.py
本项目采用GPL 许可证，欢迎任何人使用、修改和分发。
'''
import requests
import re
import os
from urllib.parse import quote
class HttpClient:
    def __init__(self):
        self.host = ""
        self.cookie = ""
        self.loginhash = ""
        self.forhash = ""
        self.name = ""
        self.key = ""
        self.signhash = ""
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
        self.signhash = re.search(r'id="JD_sign".*?href="(.*?)".*onclick', response.text).group(1)
        # print( self.signhash)
        
    def sign(self):
        url=f'https://{self.host}/{self.signhash}&inajax=1&ajaxtarget='
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
            };
        response = requests.get(url, headers=headers)
        print(response.text) 

def main():
    client = HttpClient()
    host = "ysqbbs.com"
    account=os.environ.get('YSQ_ACCOUNT')
    password=os.environ.get('YSQ_PASSWORD')
    # account=""
    # password=""
    client.setenv(host,account,password)
    client.get_login_info()
    client.login()
    client.gethash()
    client.sign()
# 运行示例
if __name__ == "__main__":
    main()
    