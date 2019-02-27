# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     crawler_51job
   Description :
   Author :       lishuai
   date：          2019/2/26
-------------------------------------------------
   Change Activity:
                   2019/2/26:
-------------------------------------------------
"""
from typing import Type

from selenium.webdriver.chrome.webdriver import WebDriver

__author__ = 'lishuai'


import requests
from lxml import etree
import re, os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import xlwt

rowTitle = ['职务名称','公司名','公司地址','工资','详细网址']
workbook = xlwt.Workbook(encoding='utf-8')

# 将Chrome设置成不加载的无界面运行状态
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-gpu')

url = "https://www.51job.com"
chrome_path = 'E:\\study_tool\\chromedriver.exe'
browser = webdriver.Chrome(chrome_path, options=chrome_options)

# 设置headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Referer': "https://www.51job.com"
}

def get_html():
    html = requests.get(url).content
    xpath_html = etree.HTML(html)
    print(xpath_html)

def get_search_url(keyword, address, salary_str):
    browser.get("https://www.51job.com")
    k_input = browser.find_element_by_id("kwdselectid")
    k_input.send_keys(keyword)
    k_input.send_keys(Keys.ENTER)
    time.sleep(1)
    ad_input = browser.find_element_by_id("work_position_input")
    ad_input.send_keys(address)
    ad_input.send_keys(Keys.ENTER)
    time.sleep(1)
    button = browser.find_element_by_link_text(salary_str)
    button.click()
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'goTop')))
    search_url = browser.current_url
    browser.close()
    return search_url

def get_page_url(url):
    url_list = [url]
    html = requests.get(url).content
    xpath_html = etree.HTML(html)
    total_page = xpath_html.xpath('//div[@class="p_in"]/span[@class="td"]/text()')[0]
    pattern = "[1-9]\d*"
    number = re.search(pattern, total_page).group()
    for n in range(2, int(number)+1):
        replace_str = "{0}.html?".format(str(n))
        new_url = url.replace("1.html?", replace_str)
        url_list.append(new_url)
    print("all page url list:", url_list)
    return url_list

def get_info_dict_list(url):
    info_dict_list = []
    html = requests.get(url).content
    xpath_html = etree.HTML(html)
    work_name_list = xpath_html.xpath('//div[@class="el"]/p[@class="t1 "]/span/a/@title')
    company_name_list = xpath_html.xpath('//div[@class="el"]/span[@class="t2"]/a/@title')
    address_name_list = xpath_html.xpath('//div[@class="el"]/span[@class="t3"]/text()')
    salary_list = xpath_html.xpath('//div[@class="el"]/span[@class="t4"]/text()')
    link_list = xpath_html.xpath('//div[@class="el"]/p[@class="t1 "]/span/a/@href')
    current_count_number = len(work_name_list)
    for n in range(current_count_number):
        info_dict = {}
        info_dict["work_name"] = work_name_list[n]
        info_dict["company_name"] = company_name_list[n]
        info_dict["address_name"] = address_name_list[n]
        info_dict["salary"] = salary_list[n]
        info_dict["link"] = link_list[n]
        info_dict_list.append(info_dict)
    return info_dict_list

def add_sheet(sheet_name, row_titles):
    sheet_info = workbook.add_sheet(sheet_name,cell_overwrite_ok=True)
    for i in range(0, len(row_titles)):
        sheet_info.write(0, i, row_titles[i])
    return sheet_info


def write_excel(data,execl_name,count=[]):
    count.append(1)
    for j in range(0, len(data)):
        data_sheet.write(len(count), j, data[j])
    workbook.save(execl_name)

if __name__ == "__main__":
    all_info_dict_list = []
    data_sheet = add_sheet('51job_crawler', rowTitle)
    search_url = get_search_url("jenkins", "上海", "1.5-2万")
    all_page_url_list = get_page_url(search_url)
    for u in all_page_url_list:
        all_info_dict_list.extend(get_info_dict_list(u))
    for info_dict in all_info_dict_list:
        info_list = [
            info_dict['work_name'],
            info_dict['company_name'],
            info_dict['address_name'],
            info_dict['salary'],
            info_dict['link'],
        ]
        write_excel(info_list, 'spider_for_51job.xls')