# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     translate_crawler
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
   File Name：     crawler_myself_test
   Description :
   Author :       t_lishu
   date：          11/5/2018
-------------------------------------------------
   Change Activity:
                   11/5/2018:
-------------------------------------------------
"""
__author__ = 't_lishu'

from urllib import request
from urllib import parse
def translate_test(translate_str):
    Request_URL = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    From_Data = {
    'i': translate_str,
    'doctype': 'json',
    }
    data = parse.urlencode(From_Data).encode('utf-8')
    response = request.urlopen(Request_URL, data)
    html = response.read().decode('utf-8')
    translate_result = eval(html)
    result = translate_result['translateResult'][0][0]['tgt']
    return result

if __name__ == '__main__':
    a = translate_test("i will take tomorrow off for personal errand")
    print(a)