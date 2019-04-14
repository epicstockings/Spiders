# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 18:07:05 2019

@author: siwo1
"""
import re
import requests
from bs4 import BeautifulSoup

url = 'https://www.aqistudy.cn/historydata/'
#获取html信息
html = requests.get(url)
#创建soup对象
soup = BeautifulSoup(html.text)
#提取html中<a> </a>之间内容，输出到lists
a_lists=soup.find_all('a')
#将正则表达式编译成Pattern对象
pattern = re.compile(r'<a href="monthdata\.php\?city=(?P<city>.*)"')
city_set = []
#对每一个'a'对象进行正则匹配，满足城市结构的append 到 city_set中
for i in a_lists:
    match = pattern.match(str(i))
    if match:
        print(match.group('city'))
        city_set.append(match.group('city'))
#去除重复城市
city_set = list(set(city_set))
#存储城市信息到txt
with open('./cities.txt' ,'w')as f:
    for city in city_set:
        f.write(city + '\n')