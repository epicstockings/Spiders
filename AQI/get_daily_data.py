# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 20:05:39 2019

@author: siwo1
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import parse
import pandas as pd

#下载城市对应月份数据
def download_city(city_set,month_set):
    count= 0
    base_url = 'https://www.aqistudy.cn/historydata/daydata.php?city='
    for city in city_set:   #####
    #city='成都'
        driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe',chrome_options=chrome_options)
        file_name = 'C:/Temp/data_out/日均值_%s.txt'%(city)
        fp = open(file_name, 'w')
        for month in month_set:
            weburl = ('%s%s&month=%s' % (base_url, parse.quote(city),month))
            driver.get(weburl)
            time.sleep(1)
            dfs = pd.read_html(driver.page_source,header=0)[0]
            if len(dfs)==0:
                driver.get(weburl)
                print('Please wait %s seconds.'%(3))
                time.sleep(3)
                dfs = pd.read_html(driver.page_source,header=0)[0]
                if len(dfs)==0:
                    print('%d---%d---%s---%s---DONE' % (count,len(dfs), city,month))
                    continue
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
            print('%d---%d---%s---%s---DONE' % (count,len(dfs), city,month))
        fp.close()
        driver.quit()
        print ('%s已经爬完！请检测！'%(city))
        count +=1
#获取城市信息
def get_city_set():
    with open('./cities.txt' ,'r')as f:
        reader = f.readlines()
    for i in range(len(reader)):
        reader[i]= reader[i].split('\n')[0]
    return reader
#获取所需要的月份
def get_month_set():
    month_set = ['201312']
    for year in [2014,2015,2016,2017,2018]:
        for month in ['01','02','03','04','05','06',
                      '07','08','09','10','11','12']:
            month_set.append('%s%s'%(year,month))
    month_set.extend(['201901','201902','201903'])
    return month_set

if __name__ == '__main__':
    #获取月份数据
    month_set=get_month_set()
    #获取城市信息
    city_set = get_city_set()
    
    #浏览器不提供可视化页面
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    
    #下载城市对应月份数据
    download_city(city_set,month_set)