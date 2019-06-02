# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     baidu_article_crawler
   Description :
   Author :       lishuai
   date：          2019/4/21
-------------------------------------------------
   Change Activity:
                   2019/4/21:
-------------------------------------------------
"""
__author__ = 'lishuai'

import requests
from lxml import etree
import re, os, time
from selenium import webdriver
from urllib import request
from bs4 import BeautifulSoup

# 将Chrome设置成不加载的无界面运行状态
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_path = 'E:\\study_tool\\chromedriver.exe'


url = "https://wenku.baidu.com/view/3d926e26482fb4daa58d4bcb.html?sxts=1555848439327"
# 设置headers
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/65.0.3325.181 Safari/537.36',
    'Referer': url,
}




def get_html_info(url):
    driver = webdriver.Chrome(chrome_path, options=chrome_options)
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    selector = etree.HTML(html)
    src_list = selector.xpath(
        '//div[@class="ppt-image-wrap"]/img/@src')
    data_src_list = selector.xpath(
        '//div[@class="ppt-image-wrap"]/img/@data-src')
    info = src_list + data_src_list
    return info


def download_ppt_picture(url_list):
    PICTURES_PATH = os.path.join(os.getcwd(), 'pictures/')
    ppt_name = "django_ppt"
    img_name = 0
    try:
        os.mkdir(PICTURES_PATH)
    except:
        pass
    ppt_path = PICTURES_PATH + ppt_name
    try:
        os.mkdir(ppt_path)
    except Exception as e:
        print("{}已存在".format(ppt_name))
    for i in url_list:
        img_name += 1
        img_data = requests.get(i, headers=headers)
        pic_path = ppt_path + '/' + str(img_name) + '.jpg'
        if os.path.isfile(pic_path):
            print("{}第{}张已存在".format(ppt_name, img_name))
            pass
        else:
            with open(pic_path, 'wb')as f:
                f.write(img_data.content)
                print("正在保存{}第{}张".format(ppt_name, img_name))
                f.close()

info = get_html_info(url)
download_ppt_picture(info)