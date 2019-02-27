# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     biqukan_crawler
   Description :
   Author :       lishuai
   date：          2019/2/27
-------------------------------------------------
   Change Activity:
                   2019/2/27:
-------------------------------------------------
"""
__author__ = 'lishuai'

# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     crawler_biqukan
   Description :
   Author :       t_lishu
   date：          12/4/2018
-------------------------------------------------
   Change Activity:
                   12/4/2018:
-------------------------------------------------
"""
__author__ = 'lishuai'

#URL：http://www.biqukan.com/1_1094/5403177.html

from urllib import request
from bs4 import BeautifulSoup
import sys

url = "https://www.biqukan.com/1_1094/"
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}

def get_response_info(url, class_):
    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    html = response.read().decode('gbk', 'ignore')
    BS = BeautifulSoup(html, 'lxml')
    string = BS.find_all(class_=class_)[0]
    info = BeautifulSoup(str(string), 'lxml')
    return info

def main(url):
    file = open('{0}.txt'.format("一念天堂"), 'w', encoding='utf-8')
    chapters_BS = get_response_info(url, class_="listmain")
    chapter_numbers = 1314
    index = 1
    begin_flag = False
    false_flag_str_list = [
        u"新书《三寸人间》发布！！！求收藏！！",
        u"《三寸人间》上架啦，已40万字，可以开宰啦~~",
        u"《三寸人间》上架啦，已40万字，可以开宰啦~~1 biqukan.com",
        ]
    for child in chapters_BS.dl.children:
        if child != '\n':
            if child.string == u"第一章 他叫白小纯":
                begin_flag = True
            if child.string in false_flag_str_list:
                begin_flag = False
            if begin_flag == True and child.a != None:
                print("come in")
                download_url = "http://www.biqukan.com" + child.a.get('href')
                download_name = child.string
                download_text = get_response_info(download_url, class_="showtxt")
                file.write(download_name + '\n\n')
                string = download_text.div.text.replace('\xa0', '')
                file.write(string)
                file.write('\n\n')
                # 打印爬取进度
                sys.stdout.write("已下载:%.3f%%" % float(index / chapter_numbers) + '\r')
                sys.stdout.flush()
                index += 1
    file.close()
if __name__ == '__main__':
    main(url)