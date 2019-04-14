# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:49:10 2019

@author: siwo
"""
import requests
from bs4 import BeautifulSoup
import re,time,json
import random
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
#获取搜索页面url
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
#拼接搜索页面url
def get_url_search(pageNumber, city,keyword):
    urls = []
    for pn in range(pageNumber):
        url = 'https://www.liepin.com/city-%s/zhaopin/pn%s/?key=%s'%(city,pn,keyword)
        urls.append(url)
    return urls

#从搜索页面获取具体招聘页面url
def get_url_info(url_search):
    html = requests.get(url_search,headers=hds[random.randint(0,len(hds)-1)]).text
    soup = BeautifulSoup(html,'lxml')
    hrefs = soup.find_all('a')
    hrefs_useful = []
    pattern = re.compile(r'https://www.liepin.com/job/.*.shtml')
    for link in hrefs:
        try:
            match = pattern.match(link.get('href'))
            if match:
                print(link.get('href'))
                hrefs_useful.append(link.get('href'))
        except:
            1
    return hrefs_useful

#对每个城市的所有搜索页面提取具体招聘页面的url，并去重
def get_city_url_info(city,url_list):
    hrefs_useful = []
    hrefs_useful_len = 0
    repeat_n = 0
    for url_search in url_list:
        hrefs_useful.extend(get_url_info(url_search))
        time.sleep(0.5)
        hrefs_useful_set = list(set(hrefs_useful))
        #判断是否多个页面没有获得新数据
        if hrefs_useful_len == len(hrefs_useful_set):
            repeat_n += 1
        else:
            repeat_n =0
        #连续n次没有新数据则返回
        if repeat_n > 10:
            print('---%s--以超过%s个页面没有更新，退出'%(city,repeat_n))
            break
        hrefs_useful_len = len(hrefs_useful_set)
        print('---%s----已经完成，有---%s---页面'%(city,len(hrefs_useful_set)))
    return hrefs_useful_set
        
    
cities = ['sh','bj','sz','gz','xiamen','hz','zhengzhou','nj','cq','tj','cd',
          'suzhou','dl','jinan','ningbo','wuxi','qingdao','shenyang',#'taizhou',
          'xian','wuhan']    #'sh',
key = '气象'
url_list = {}
url_list_city_info = {}
for city in cities:
    url_list[city] = get_url_search(99, city,key)
    url_list_city_info[city] = get_city_url_info(city,url_list[city])
    print('%s--爬取完成，获得--%s--个页面'%(city , len(url_list_city_info[city])))

path_out = r'C:\nriet\自娱自乐\爬虫\liepin_info_url_%s.json'%key
with open(path_out,'w')as f:
    json.dump(url_list_city_info,f)
    print('写入文件完成-----')


#hrefs_useful = []
#hrefs_useful_len = 0
#repeat_n = 0
#city = 'sh'
#for url_search in url_list[city]:
#    hrefs_useful.extend(get_url_info(url_search))
#    time.sleep(2)
#    hrefs_useful_set = list(set(hrefs_useful))
#    #判断是否多个页面没有获得新数据
#    if hrefs_useful_len == len(hrefs_useful_set):
#        repeat_n += 1
#    else:
#        repeat_n =0
#    #连续5次没有新数据则返回
#    if repeat_n > 5:
#        print('---%s--以超过5个页面没有更新，退出'%(city))
#        break
#    hrefs_useful_len = len(hrefs_useful_set)
#    print('---%s----已经完成，有---%s---页面'%(city,len(hrefs_useful_set)))
#hrefs_useful_set = list(set(hrefs_useful))
    
#url_search = url_list[0]
#html = requests.get(url_search,headers=hds[random.randint(0,len(hds)-1)]).text
#soup = BeautifulSoup(html,'lxml')
#hrefs = soup.find_all('a')
#hrefs_useful = []
#pattern = re.compile(r'https://www.liepin.com/job/.*.shtml')
#for link in hrefs:
#    try:
#        match = pattern.match(link.get('href'))
#        if match:
#            print(link.get('href'))
#            hrefs_useful.append(link.get('href'))
#    except:
#        1
#    print(link.get('href'))
#soup.title
# In[]
    
def get_job_url(city_number,key):
    url_root = 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&dqs=%s&key=%s'%(city_number,key)
    url_tmp = url_root
    pn = 1
    hrefs_useful = []
    repeat_n = 0
    hrefs_useful_len = 0
    while pn < 99:
        driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe',
                                  chrome_options=chrome_options)
        
        driver.get(url_tmp)
        time.sleep(1)
    
        html = driver.page_source
        soup = BeautifulSoup(html,'lxml')
        hrefs = soup.find_all('a')
        
        pattern = re.compile(r'https://www.liepin.com/job/.*.shtml')
        pattern_end = re.compile(r'.*curPage=%d'%pn)
        for link in hrefs:
            try:
                match = pattern.match(link.get('href'))
                if match:
    #                print(link.get('href'))
                    hrefs_useful.append(link.get('href'))
                match_end = pattern_end.match(link.get('href'))
                if match_end:
                    next_url = link.get('href')
                    
                    
                    url_tmp = 'https://www.liepin.com' + next_url
                    
    #                print(url_tmp)
                    break
            except:
                1
        pn += 1
        driver.quit()
        hrefs_useful_set = list(set(hrefs_useful))
        #判断是否多个页面没有获得新数据
        if hrefs_useful_len == len(hrefs_useful_set):
            repeat_n += 1
        else:
            repeat_n =0
        #连续5次没有新数据则返回
        if repeat_n > 5:
            print('---%s--以超过5个页面没有更新，退出'%(city_number))
            return hrefs_useful_set
        hrefs_useful_len = len(hrefs_useful_set)
        print('---%s---%s---已经完成，有---%s---页面'%(city_number,pn-1,len(hrefs_useful_set)))
    return hrefs_useful_set
#chrome_options = Options()
#chrome_options.add_argument('--headless')
##dqs = ['010','030','210040','020','060020','060080','070020','170020',
##       '050020','050090','040','280020']
#dqs = ['050090','280020']
#
##city_number = '010'
#hrefs_useful = {}
#time0 = time.time()
#key = 'python'
#for city_number in dqs:
#    time_tmp = time.time()
#    hrefs_useful_tmp = get_job_url(city_number,key)
#    hrefs_useful[city_number] = hrefs_useful_tmp
#    time_now = time.time()
#    print('------------------------------')
#    print('%s--已经完成，用时--%s--总用时--%s'%(city_number,time_now-time_tmp,time_now-time0))
#    print('------------------------------')
    
    
#url_root = 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&dqs=%s&key=python'%(city_number)
#url_tmp = url_root
#pn = 1
#hrefs_useful = []
#while pn < 99:
#    driver = webdriver.Chrome('C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe',
#                              chrome_options=chrome_options)
#    
#    driver.get(url_tmp)
#    time.sleep(1)
#
#    html = driver.page_source
#    soup = BeautifulSoup(html,'lxml')
#    hrefs = soup.find_all('a')
#    
#    pattern = re.compile(r'https://www.liepin.com/job/.*.shtml')
#    pattern_end = re.compile(r'.*curPage=%d'%pn)
#    for link in hrefs:
#        try:
#            match = pattern.match(link.get('href'))
#            if match:
##                print(link.get('href'))
#                hrefs_useful.append(link.get('href'))
#            match_end = pattern_end.match(link.get('href'))
#            if match_end:
#                next_url = link.get('href')
#                
#                
#                url_tmp = 'https://www.liepin.com' + next_url
#                
##                print(url_tmp)
#                break
#        except:
#            1
#    pn += 1
#    driver.quit()
##    time.sleep(1)
#    hrefs_useful_set = list(set(hrefs_useful))
#    print('---%s---已经完成，有---%s---页面'%(pn-1,len(hrefs_useful_set)))
#    print(link.get('href'))    
#curPage=3
# In[]
#n=1
#while n<10:
#    for i in range(n):
#        print(i)
#        break
#    n+=1