# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import time
import requests
import re
import random
import sys
import io

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
         'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
         'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
         (KHTML, like Gecko) Element Browser 5.0', \
         'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
         'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
         'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
         'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
         Version/6.0 Mobile/10A5355d Safari/8536.25', \
         'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
         Chrome/28.0.1468.0 Safari/537.36', \
         'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

def getHtmlText(url):
    try:
        r = requests.get(url, timeout=30, headers={'user-agent':user_agents[random.randint(0, 9)]})
        # 如果状态码不是200 则应发HTTOError异常
        r.raise_for_status()
        # 设置正确的编码方式
        r.encoding = 'utf-8'
        return r.text
    except Exception as e:
        print(e)
        return "Something Wrong!"

def getContent(url):
    html = getHtmlText(url)
    print(html)
    soup = BeautifulSoup(html, 'lxml')
    li = soup.find('div', attrs={'id': 'ires'})
    #if li is None: return ""
    cite = li.find('cite')
    cite = re.sub(r"</?cite>|</?b>", "", str(cite))
    return cite

def main(base_url, fin, fout):
    cnt = 0
    for line in fin:
        cnt += 1
        if cnt % 50 == 0: print(cnt)
        line = line.decode("utf-8")
        for i in range(2010, 2020):
            url = base_url + line.strip().split(",")[1] + str(i) + '&num=1'
            content = getContent(url)
            print(content)
            fout.write((line.strip().split(",")[1] + '***' + str(i) + '***' + content + '\n').encode("utf-8"))
    print("会议信息已保存完毕！")

base_url = "https://www.google.com.hk/search?q="
conf = open("conference.csv", "rb")

if __name__ == '__main__':
    main(base_url, conf, open("conf_home.csv","wb+"))