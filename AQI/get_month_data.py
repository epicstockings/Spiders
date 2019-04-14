# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 18:07:05 2019

@author: siwo1
"""
import re,time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import parse
import pandas as pd

#获取城市信息
def get_city_set():
    with open('./cities.txt' ,'r')as f:
        reader = f.readlines()
    for i in range(len(reader)):
        reader[i]= reader[i].split('\n')[0]
    return reader
#获取城市信息
city_set = get_city_set()

#浏览器不提供可视化页面
chrome_options = Options()
chrome_options.add_argument('--headless')

count=0
city_month_data = []

file_name = 'C:/Temp/data_out/全国城市空气污染月均数据.txt'
fp = open(file_name, 'w')
#月均数据
for city in city_set:
#    city = '南京'
    #组成城市月均值url
    url = 'https://www.aqistudy.cn/historydata/monthdata.php?city=%s'%(city)
    #打开浏览器
    driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe',chrome_options=chrome_options)
    #访问对应url
    driver.get(url)
    #等待浏览器加载页面---------重要-----------
    time.sleep(1)
    #获取页面中的表格
    dfs = pd.read_html(driver.page_source,header=0)[0]
    #判断dfs是否有数据，没有数据则增加等待时间
    if len(dfs)==0:
        driver.get(url)
        print('Please wait %s seconds.'%(3))
        time.sleep(3)
        dfs = pd.read_html(driver.page_source,header=0)[0]
    #存储数据到文件
    for j in range(0,len(dfs)):
        date = dfs.iloc[j,0]
        aqi = dfs.iloc[j,1]
        grade = dfs.iloc[j,2]
        pm25 = dfs.iloc[j,3]
        pm10 = dfs.iloc[j,4]
        so2 = dfs.iloc[j,5]
        co = dfs.iloc[j,6]
        no2 = dfs.iloc[j,7]
        o3 = dfs.iloc[j,8]
        fp.write(('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (city,date,aqi,grade,pm25,pm10,so2,co,no2,o3)))
    print('%d---%s---DONE' % (len(dfs), city))
    #关闭浏览器
    driver.quit()
    count +=1
print ('%s已经爬完！请检测！'%(city))
fp.close()