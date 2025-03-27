import re
import requests
import os

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
        self.name=name
        self.key=key
    def getkey(self):
        url = f"https://{self.host}/k_misign-sign.html"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': self.host,
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        cookies = response.headers.get("Set-Cookie", "")
        self.cookie = re.sub(r'expires.*?;|path.*?,|path=/|Max.*?;|secure| ', '', cookies)
        self.cookie = self.cookie.replace(";;", ";")
        cookie_pairs = self.cookie.split(';')
        unique_cookies = {}
        for pair in cookie_pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                unique_cookies[key] = value
        self.cookie = ';'.join([f'{key}={value}' for key, value in unique_cookies.items()])
        self.cookie += ';YPSa_2132_sendmail=1;'

    def login_1(self):
        url = f"https://{self.host}/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': self.host,
            'Cookie': self.cookie,
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        response = requests.get(url, headers=headers)
        cookies = response.headers.get("Set-Cookie", "")
        self.cookie += re.sub(r'expires.*?;|path.*?,|path=/|Max.*?;|secure| ', '', cookies)
        self.cookie = self.cookie.replace(";;", ";")
        cookie_pairs = self.cookie.split(';')
        unique_cookies = {}
        for pair in cookie_pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                unique_cookies[key] = value
        self.cookie = ';'.join([f'{key}={value}' for key, value in unique_cookies.items()])
        self.cookie = self.cookie.replace("YPSa_2132_sendmail=1", "")
        resdata = response.text
        self.loginhash = re.search(r'loginhash=(.*?)"', resdata).group(1)
        self.forhash = re.search(r'formhash" value="(.*?)"', resdata).group(1)

    def login_2(self):
        url = f'https://{self.host}/member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash={self.loginhash}&inajax=1'
        headers = {
            'Host': self.host,
            'Origin': 'https://ysqbbs.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Referer': 'https://ysqbbs.com/portal.php',
            'Cookie': self.cookie,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = f'formhash={self.forhash}&referer=https%3A%2F%2Fysqbbs.com%2Fportal.php&username={self.name}&password={self.key}&questionid=0&answer='
        response = requests.post(url, headers=headers, data=data)
        cookies = response.headers.get("Set-Cookie", "")
        self.cookie += re.sub(r'expires.*?;|path.*?,|path=/|Max.*?;|secure| ', '', cookies)
        self.cookie = self.cookie.replace(";;", ";")
        cookie_pairs = self.cookie.split(';')
        unique_cookies = {}
        for pair in cookie_pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                if key not in ['YPSa_2132_loginuser', 'YPSa_2132_activationauth', 'YPSa_2132_pmnum']:
                    unique_cookies[key] = value
        self.cookie = ';'.join([f'{key}={value}' for key, value in unique_cookies.items()])

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
            'Referer': 'https://ysqbbs.com/k_misign-sign.html',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        }
        response = requests.get(url, headers=headers)
        resdata = response.text
        self.signhash = re.search(r'id="JD_sign".*?href=(.*?)onclick', resdata).group(1)
        self.signhash=self.signhash.replace("\"","").replace(" ","")

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
            'Host' : 'ysqbbs.com',
            'sec-ch-ua-platform' : '"macOS"',
            'DNT' : '1',
            'Accept-Language' : 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Accept' : '*/*',
            'Referer' : 'https://ysqbbs.com/k_misign-sign.html'
            };
        response = requests.get(url, headers=headers)
        print(response.status_code) 

# 示例用法
def main():
    client = HttpClient()
    host = "srcbbs.com"
    account=os.environ.get('YSQ_ACCOUNT')
    password=os.environ.get('YSQ_PASSWORD')
    client.setenv(host,account,password)
    client.getkey()
    client.login_1()
    client.login_2()
    client.gethash()
    client.sign()

# 运行示例
if __name__ == "__main__":
    main()
    