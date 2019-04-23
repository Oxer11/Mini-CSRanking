# -*-coding:utf-8-*-
import xml.sax

YEAR_THRESHOLD = 2015
datas = set()
#OUT = open("paper.csv","wb")
OUT = open("paper_author.csv","wb")
dict = []
book_title = {}
Final_data = []

class MovieHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.title = ""
        self.ee = ""
        self.year = ""
        self.journal = ""
        self.author = []
        self.entry = {}
        self.key = 0
        self.booktitle = ""

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag in ["inproceedings", "proceedings"]:
            self.key = 1
            self.entry = {}

    # 元素结束事件处理
    def endElement(self, tag):
        if self.CurrentData == 'author': self.entry["author"] = self.author
        elif self.CurrentData == "title": self.entry["title"] = self.title
        elif self.CurrentData == "ee": self.entry["ee"] = self.ee
        elif self.CurrentData == "journal": self.entry["journal"] = self.journal
        elif self.CurrentData == "year": self.entry["year"] = int(self.year)
        elif self.CurrentData == "booktitle": self.entry["booktitle"] = self.booktitle
        elif self.key == 1:
            global dict
            dict.append(self.entry)
            self.key = 0
            self.author = []
        self.CurrentData = ""

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "title":
            self.title = content
        elif self.CurrentData == "ee":
            self.ee = content
        elif self.CurrentData == "year":
            self.year = content
        elif self.CurrentData == "journal":
            self.journal = content
        elif self.CurrentData == "booktitle":
            self.booktitle = content
        elif self.CurrentData == 'author':
            self.author.append(content)

if __name__ == "__main__":
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MovieHandler()
    parser.setContentHandler(Handler)
    parser.parse("dblp2.xml")

    print(len(dict))
    cnt = 0
    for item in dict:
        if item['year'] >= YEAR_THRESHOLD:
            if 'title' not in item.keys(): continue
            if 'ee' not in item.keys(): continue
            if 'author' not in item.keys(): continue
            '''
            STR = item['title'] + "***" + str(item['year']) + "***" + item["ee"] + "***" + item["booktitle"] + "\n"
            OUT.write(STR.encode("utf-8"))
            
            '''
            #'''
            for i in item['author']:
                STR = item['title'] + "***" + i + "\n"
                OUT.write(STR.encode("utf-8"))
                cnt += 1
            #'''
            book_title[item['booktitle']] = 1

    print([k for k in book_title])
    print(cnt)
