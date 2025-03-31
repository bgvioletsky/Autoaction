'''
Author: bgcode
Date: 2024-10-28 15:54:20
LastEditTime: 2025-03-31 10:00:14
LastEditors: bgcode
Description: 描述
FilePath: /Autoaction/python/sxmd.py
本项目采用GPL 许可证，欢迎任何人使用、修改和分发。
'''
import re
import http.client
import os

class HttpClient:
    def __init__(self):
        self.cookie = ""
        self.formhash = ""
        self.true = ""
        self.subt = ""
        self.result=""

    def login(self, host, account, password):
        login_url = f"/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LxEUe&mobile=2"
        data = f"formhash=&referer=http%3A%2F%2F{host}%2Fplugin.php%3Fid%3Ddsu_paulsign%3Asign&fastloginfield=username&cookietime=2592000&username={account}&password={password}&questionid=0&answer=&submit=true"
        headers = {
            "Host": host,
            "Referer": f"http://{host}/member.php?mod=logging&action=login&mobile=2",
            "Cookie": self.cookie,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Snapchat/10.77.5.59 (like Safari/604.1)",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        conn = http.client.HTTPConnection(host)
        conn.request("POST", login_url, body=data, headers=headers)
        resp = conn.getresponse()
        resdata = resp.read().decode('utf-8')
        if "欢迎您回来" in resdata:
            set_cookie = resp.getheader("Set-Cookie", "")
            self.cookie = re.sub(r'expires.*?;|path.*?,|path=/', '', set_cookie)
            return True
        else:
            return False

    def getformhash(self, host):
        url = f"/plugin.php?id=dsu_paulsign:sign&mobile=yes"
        headers = {
            "Host": host,
            "Referer": f"http://{host}/member.php?mod=logging&action=login&mobile=2",
            "Cookie": self.cookie,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Snapchat/10.77.5.59 (like Safari/604.1)",
        }

        conn = http.client.HTTPConnection(host)
        conn.request("GET", url, headers=headers)
        resp = conn.getresponse()
        resdata = resp.read().decode('utf-8')
        self.formhash = re.search(r'<input type="hidden" name="formhash" value="(.+?)" />', resdata).group(1)
        self.true = re.search(r'<div class="bm_h">(.+?)</div>', resdata, re.DOTALL).group(1)
        return True

    def sign(self, host):
        url = f"/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=0&inajax=0&mobile=yes"
        data = f"formhash={self.formhash}&qdxq=kx"
        headers = {
            "Host": host,
            "Referer": f"http://{host}/plugin.php?id=dsu_paulsign:sign&mobile=yes",
            "Cookie": self.cookie,
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Snapchat/10.77.5.59 (like Safari/604.1)",
        }

        conn = http.client.HTTPConnection(host)
        conn.request("POST", url, body=data, headers=headers)
        resp = conn.getresponse()
        resdata = resp.read().decode('utf-8')
        message = re.search(r'<div id="messagetext">.*?<p>(.+?)</p>', resdata, re.DOTALL)
        if message:
            self.subt = "签到成功!"
            return True
        else:
            self.subt = "签到失败!"
            return False

    def info(self,host):
    
            url = f"/home.php?mod=space&uid=4402227&do=profile&mobile=yes"
            headers = {
                "Host": host,
                "Referer": f"http://{host}/member.php?mod=logging&action=login&mobile=2",
                "Cookie": self.cookie,
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Mobile/15E148 Snapchat/10.77.5.59 (like Safari/604.1)",
            }

            conn = http.client.HTTPConnection(host)
            conn.request("GET", url, headers=headers)
            resp = conn.getresponse()
            resdata = resp.read().decode('utf-8')
            message = re.search(r'<li><em>金币<\/em>(.+?) 枚<\/li>', resdata)
            if message:
                self.result += "金币:" + message.group(1)
                return True
            else:
                return False


# 示例用法
def main():
    client = HttpClient()
    host = "www.txtnovel.vip"
    account=os.environ.get('SXMD_ACCOUNT')
    password=os.environ.get('SXMD_PASSWORD')
    account="bgcode"
    password="snC$3LfrxVq7f"
    client.login(host, account, password)
    client.getformhash(host)
    client.sign(host)
    client.info(host)
    print(client.result)
    return client.result
# 运行示例
if __name__ == "__main__":
    main()