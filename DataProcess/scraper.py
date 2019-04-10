# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import time
import requests
import re
import sys
import io

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def getHtmlText(url):
    try:
        r = requests.get(url, timeout=30)
        # 如果状态码不是200 则应发HTTOError异常
        r.raise_for_status()
        # 设置正确的编码方式
        r.encoding = 'utf-8'
        return r.text
    except:
        return "Something Wrong!"

def getContent(url):
    html = getHtmlText(url)
    soup = BeautifulSoup(html, 'lxml')
    li = soup.find('div', attrs={'id':'ires'})
    cite = li.find('cite')
    cite = re.sub(r"</?cite>|</?b>", "", str(cite))
    return cite

def main(base_url, fin, fout):
    cnt = 0
    for line in fin:
        cnt += 1
        if cnt % 50 == 0: print(cnt)
        line = line.decode("utf-8")
        url = base_url + 'CS ' + line.strip() + '&num=1'
        print(url)
        content = getContent(url)
        print(content)
        fout.write((line.strip() + ',' + content + '\n').encode("utf-8"))
    print("学校信息已保存完毕！")

base_url = "https://www.google.com.hk/search?q="
institution = open("institution.csv", "rb")

if __name__ == '__main__':
    main(base_url, institution, open("institution_homepage.csv","wb+"))