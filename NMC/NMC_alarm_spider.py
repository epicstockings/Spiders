# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 20:33:35 2019

@author: siwo1
"""

import requests
from bs4 import BeautifulSoup
import re,time
import json
import random
import os

#头
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]
#解析每个具体警报页面，返回主要信息
def get_url_info(url):
    html = requests.get(url,headers=hds[random.randint(0,len(hds)-1)]).text
    soup = BeautifulSoup(html,'lxml')
    #动作：解除、发布
    action  = soup.table.td.span.text
    #站点
    station = soup.table.td.h2.text.split(action)[0]
    #等级
    level   = soup.table.td.h2.text.split(action)[1][0:2]
    #预警类别
    category= soup.table.td.h2.text.split(action)[1][2:]
    #时间
    info_time = soup.table.find_all('td',style="color: #999")[0].text
    #完整信息
    alarmtext_mb = soup.find_all('div',class_ = "alarmtext mb")[0].text
    #防御指南
    try:
        alarmtext = soup.find_all('div',class_ = "alarmtext")[1].text
    except:
        alarmtext = 'NA'
#        os._exit(0)
    print('%s-%s-%s-%s-%s'%(info_time,station,action,level,category))
    return [station, action, level, category, info_time, alarmtext_mb, alarmtext]
    
#解析搜索页面，返回页面中具体警报信息的url list
def get_url_list(url):
    a_href_list = soup.find_all('a',href = re.compile('/f/alarm/'))
    out_list = []
    for i in a_href_list:
        out_list.append(i['href'])
    return out_list
# In[]获取数据
#第一个页面，为了确定网站页码总数
page_url_1 = r'http://m.nmc.cn/f/alarm.html?pageNo=1'
url_NMC = 'http://m.nmc.cn'
#确定页码总数pn_end
html = requests.get(page_url_1,headers=hds[random.randint(0,len(hds)-1)]).text
soup = BeautifulSoup(html,'lxml')
pn_end = soup.find_all('a',href = re.compile('/f/alarm.html\?'))[-1]['href'].split('=')[-1]

#初始化网站现有所有警报url list
info_url_list = []
for pn in range(int(pn_end)):
    page_url = r'http://m.nmc.cn/f/alarm.html?pageNo=%s'%(pn+1)
    info_url_list.extend(get_url_list(page_url))

#初始化输出
out_info = []
for i in info_url_list:
    url_tmp = url_NMC + i
    out_info.append(get_url_info(url_tmp))
time_now_str = time.strftime("%Y%m%d%H", time.localtime())
out_dict = {time_now_str : out_info}
# In[]存储数据

path_out = 'NMC_alarm_%s.json'%time_now_str
with open(path_out,'w')as f:
    json.dump(out_dict,f)

# In[]读取测试
with open(path_out,'r')as f:
    aa= json.load(f)
