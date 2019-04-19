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
    print(soup.prettify())
    li = soup.find('div', attrs={'class':'gs_ri'})
    print(li)
    #cite = li.find('cite')
    #cite = re.sub(r"</?cite>|</?b>", "", str(cite))
    #return cite

def main(base_url, fin, fout):
    cnt = 0
    for line in fin:
        cnt += 1
        if cnt > 1: break
        if cnt % 50 == 0: print(cnt)
        line = line.decode("utf-8")
        url = base_url + line.strip().split("***")[0] + '&btn='
        print(url)
        content = getContent(url)
        #print(content)
        #fout.write((line.strip() + ',' + content + '\n').encode("utf-8"))
    print("论文信息已保存完毕！")

base_url = "https://scholar.google.com/scholar?&hl=en&num=1&q="
paper = open("paper.csv", "rb")

if __name__ == '__main__':
    main(base_url, paper, open("paper_refer.csv","wb+"))