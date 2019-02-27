# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     aiqiyi_TV_info_crawler
   Description :
   Author :       lishuai
   date：          2019/2/27
-------------------------------------------------
   Change Activity:
                   2019/2/27:
-------------------------------------------------
"""
__author__ = 'lishuai'

#爬取爱奇艺电视剧
#目标网址：http://list.iqiyi.com/www/2/-------------11-1-1-iqiyi--.html

import requests
from lxml import etree
import re, os, time
from selenium import webdriver

# 将Chrome设置成不加载的无界面运行状态
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')
chrome_path = 'E:\\study_tool\\chromedriver.exe'

# 设置headers
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/65.0.3325.181 Safari/537.36',
    'Referer': "http://www.mmjpg.com"
}
class TV_Spider(object):
    def __init__(self,page_number):
        self.page_number = page_number
        self.page_urls = []
        self.tv_urls = []
        self.tv_name = []
        self.dramas_dict = {}

    def get_page_urls(self):
        if int(self.page_number) > 0:
            page_url = "http://list.iqiyi.com/www/2/-------------11-{0}-1-iqiyi--.html".format(self.page_number)
            self.page_urls.append(page_url)

    def get_tv_urls(self):
        for page_url in self.page_urls:
            html = requests.get(page_url).content
            xpath_html = etree.HTML(html)
            self.tv_urls += (xpath_html.xpath('//div[@class="mod-listTitle_left"]/p[@class="site-piclist_info_title "]/a/@href'))

    def get_dramas_urls(self):
        show_url_list = new_show_url_list = []
        driver = webdriver.Chrome(chrome_path, options=chrome_options)
        for tv_url in self.tv_urls:
            print(tv_url)
            html = requests.get(tv_url).content
            xpath_html = etree.HTML(html)
            show_name = xpath_html.xpath('//h1/a/@title')
            show_numbers = xpath_html.xpath('//i[@class="title-update-num"]/text()')[0]
            print("show_numbers:", show_numbers)
            driver.get(tv_url)
            time.sleep(3)
            if int(show_numbers) < 51:
                driver.find_element_by_xpath('//ul[@class="albumTabPills  fl"]/li[@data-avlist-page="1"]').click()
                time.sleep(3)
                html = driver.page_source
                selector = etree.HTML(html)
                check_list_part1 = selector.xpath(
                    '//ul[@class="album-numlist clearfix"]/li[@class="album_item"]/a/@href')[0:int(show_numbers)]
                show_url_list.extend(check_list_part1)
            elif 50 < int(show_numbers) < 100:
                driver.find_element_by_xpath('//ul[@class="albumTabPills  fl"]/li[@data-avlist-page="2"]').click()
                time.sleep(3)
                html = driver.page_source
                selector = etree.HTML(html)
                check_list_part2 = selector.xpath(
                    '//ul[@class="album-numlist clearfix"]/li[@class="album_item"]/a/@href')[0:int(show_numbers)-50]
                show_url_list.extend(check_list_part2)
            else:
                driver.find_element_by_xpath('//ul[@class="albumTabPills  fl"]/li[@data-avlist-page="3"]').click()
                time.sleep(3)
                html = driver.page_source
                selector = etree.HTML(html)
                check_list_part3 = selector.xpath(
                    '//ul[@class="album-numlist clearfix"]/li[@class="album_item"]/a/@href')[0:int(show_numbers)-100]
                show_url_list.extend(check_list_part3)
            self.dramas_dict = {show_name[0]: new_show_url_list}
            print("dramas_dict:", self.dramas_dict)

    def download_video(self):
        pass

    def execut_spider(self):
        self.get_page_urls()
        self.get_tv_urls()
        self.get_dramas_urls()


S = TV_Spider(1)
page_urls = S.execut_spider()