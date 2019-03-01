# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     download_m3u8_video
   Description :
   Author :       lishuai
   date：          2019/3/1
-------------------------------------------------
   Change Activity:
                   2019/3/1:
-------------------------------------------------
"""
__author__ = 'lishuai'

import os, sys, re
import requests
from lxml import etree
import time

video_url = "https://jzav-999.com/share/e7LEcdWoP5zeARoJ"

headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

def get_source_m3u8():
    #source_m3u8 = "https://jzav-999.com/ppvod/BIaKOArD.m3u8"
    redirecturl = ppvod_str = ""
    try:
        html = requests.get(video_url, headers=headers, timeout=10).content
        selector = etree.HTML(html)
        script_info = selector.xpath('//script[@type="text/javascript"]/text()')
        script_info_list = script_info[0].split('\r\n\t\tvar')
        for info in script_info_list:
            if "redirecturl" in info:
                redirecturl = info.split('=')[-1].strip(';').split('"')[1]
            if "ppvod" in info and ".m3u8" in info:
                ppvod_str = info.split('=')[-1].strip(';').split('"')[1]
        source_m3u8 = redirecturl + ppvod_str
        print(source_m3u8)
        return source_m3u8, redirecturl
    except:
        print("can not find script info")
        sys.exit(1)

def get_redirect_m3u8(source_m3u8, redirecturl):
    #redirect_m3u8 = "https://jzav-999.com/ppvod/EuC5Rmto.m3u8"
    try:
        html = requests.get(source_m3u8, headers=headers, timeout=10).text
        html_str_list = html.strip().split('\n')
        redirect_str = html_str_list[-1]
        redirect_m3u8 = redirecturl + redirect_str
        print(redirect_m3u8)
        return redirect_m3u8
    except:
        print("can not find redirect m3u8")
        sys.exit(1)

def get_m3u8_video_ts(redirect_m3u8, redirecturl):
    m3u8_video_ts_list = []
    try:
        html = requests.get(redirect_m3u8, headers=headers, timeout=10).text
        pattern = re.compile(r"(.*?).ts")
        result = pattern.findall(html)
        for r in result:
            m3u8_video_ts = redirecturl + r + ".ts"
            m3u8_video_ts_list.append(m3u8_video_ts)
        print(m3u8_video_ts_list)
        return m3u8_video_ts_list
    except:
        print("can not find m3u8 info")
        sys.exit(1)

def download_ts(m3u8_video_ts_list):
    download_path = 'E:/video_download/m3u8_vedio/'
    source_path = 'm3u8_video'
    for ts_url in m3u8_video_ts_list:
        video_name = ts_url.split('/')[-1]
        try:
            response = requests.get(ts_url, headers=headers, timeout=10)
            if response.status_code == 200:
                video_path = download_path + video_name
                print('正在下载', video_path)
                with open(download_path + video_name, 'wb') as f:
                    f.write(response.content)
                    f.close()
                print("download success")
                merge_file(download_path, source_path)
        except:
            print("download failure")
            sys.exit(1)

def merge_file(download_path, source_path):
    os.chdir(download_path)  # 修改当前工作目录
    merge_cmd = 'copy /b ' + '*.ts video' + '_' + source_path + '.mp4'
    split_cmd = 'del /Q ' + '*.ts'
    os.system(merge_cmd)
    os.system(split_cmd)


if __name__ == "__main__":
    source_m3u8, redirecturl = get_source_m3u8()
    redirect_m3u8 = get_redirect_m3u8(source_m3u8, redirecturl)
    m3u8_video_ts_list = get_m3u8_video_ts(redirect_m3u8, redirecturl)
    download_ts(m3u8_video_ts_list)
