# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 18:28:22 2019

@author: siwo1
"""

import requests
from bs4 import BeautifulSoup
import re,time
import json
import random
import pandas as pd

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

def get_url_info(url,key_word,city):
    html = requests.get(url,headers=hds[random.randint(0,len(hds)-1)]).text
    soup = BeautifulSoup(html,'lxml')
    
    ## In[] 从html中提取关键信息
    #招聘岗位简要内容
    job_name = soup.h1.text
    try:
    #公司
        company = soup.h3.find_all(href=re.compile("https://www.liepin.com/company/"))[0].text
    except:
        return ['该职位已结束']
    #薪酬待遇
    salary = soup.find_all("p", "job-item-title")[0].text.split('\r')[0]
    try:
    #岗位所在位置
        position = soup.find_all("p", "basic-infor")[0].a.text
    except:
        position = 'nan'
    #发布时间
    time_pub = soup.find_all("p", "basic-infor")[0].time['title']
    #岗位简要要求
    job_qualifications = '\t'.join(list(filter(None, soup.find_all("div", "job-qualifications")[0].text.split('\n'))))
    try:
    #岗位优势
        com_tag_list = '\t'.join(list(filter(None, soup.find_all("ul", "comp-tag-list clearfix")[0].text.split('\n'))))
    except:
        com_tag_list = 'nan'
    #岗位详细描述
    content_word = soup.find_all("div", "content content-word")[0].text
    try:
    #公司详细描述
        info_word = soup.find_all("div", "info-word")[0].text
    except:
        info_word = 'nan'
    #公司url
    url_com = soup.h3.find_all(href=re.compile("https://www.liepin.com/company/"))[0]['href']
    #公司所在行业、公司规模、公司地址
    pattern_field = re.compile(r'行业')
    pattern_com_size = re.compile(r'公司规模')
    pattern_location = re.compile(r'公司地址')
    field = 'nan'
    com_size = 'nan'
    location = 'nan'
    for li in soup.find_all("ul", "new-compintro")[0].find_all('li'):
        if pattern_location.match(li.text):
            location = li.text.split('：')[-1]
        elif pattern_com_size.match(li.text):
            com_size = li.text.split('：')[-1]
        else:
            try:
                field = li.a.text
            except:
                field = li.text.split('：')[-1]
    return [url,key_word,city,job_name,company,
            salary,position,time_pub,job_qualifications,com_tag_list,
            content_word,info_word,url_com,field,com_size,location]#
    
key_word = '气象'
#提取每个详细招聘页面url list信息
path_in = r'C:\nriet\自娱自乐\爬虫\liepin_info_url_%s.json'%key_word
with open(path_in,'r')as f:
    url_list_city_info = json.load(f)
    print('读取文件完成-----')

cities = ['xian','jinan','sh','bj','sz','gz','xiamen','hz','zhengzhou','nj','cq','tj','cd',
          'suzhou','dl','ningbo','wuxi','qingdao','shenyang',#'taizhou',
          'wuhan']
#cities = ['xian','jinan','sh','bj','sz','gz','xiamen','hz','zhengzhou','nj','cq','tj','cd']
url_list_city = list(url_list_city_info.keys())

name=['url','key_word','city','job_name','company',
      'salary','position','time_pub','job_qualifications','com_tag_list',
      'content_word','info_word','url_com','field','com_size','location']
#city = 'bj'
for city in cities:
#    city = 'ningbo'
    time0 = time.time()
    out_list = []
    count = 0
    for url in url_list_city_info[city]:
        out_list.append(get_url_info(url,key_word,city))
        print('%s--%s--爬取完成'%(count,url))
        count += 1
    print('---%s---%s---信息完成'%(city,len(url_list_city_info[city])))
    print('用时--%dmin'%((time.time()-time0)/60))
    
    #存储
    pathout = 'C:/nriet/自娱自乐/爬虫/liepin_job_info_%s_%s.csv'%(city,key_word)
    test=pd.DataFrame(columns=name,data=out_list)
    test.to_csv(pathout,encoding='utf-8')
#    with open(pathout , 'w',encoding='utf-8')as f:
#        for i in out_list:
#            f.write('\t\t\t'.join(i) + '\t\t\n\n')
## In[]获取html
#time0 = time.time()
#url = url_list_city_info[city][0]
#html = requests.get(url,headers=hds[random.randint(0,len(hds)-1)]).text
#soup = BeautifulSoup(html,'lxml')
#
### In[] 从html中提取关键信息
#job_name = soup.h1.text
#company = soup.h3.find_all(href=re.compile("https://www.liepin.com/company/"))[0].text
#salary = soup.find_all("p", "job-item-title")[0].text.split('\r')[0]
#position = soup.find_all("p", "basic-infor")[0].a.text
#time_pub = soup.find_all("p", "basic-infor")[0].time['title']
#job_qualifications = '\t'.join(list(filter(None, soup.find_all("div", "job-qualifications")[0].text.split('\n'))))
#com_tag_list = '\t'.join(list(filter(None, soup.find_all("ul", "comp-tag-list clearfix")[0].text.split('\n'))))
#content_word = soup.find_all("div", "content content-word")[0].text
#info_word = soup.find_all("div", "info-word")[0].text
#url = url_each
#url_com = soup.h3.find_all(href=re.compile("https://www.liepin.com/company/"))[0]['href']
#field = soup.find_all("ul", "new-compintro")[0].a.text
#com_size = soup.find_all("ul", "new-compintro")[0].find_all('li')[1].text.split('：')[-1]
#location = soup.find_all("ul", "new-compintro")[0].find_all('li')[2].text.split('：')[-1]
#
#print(time.time()-time0)
## In[]将关键信息存储
## 连接mysql，括号内是服务器地址, 端口号, 用户名，密码，存放数据的数据库
#conn = mysql.connector.connect(host='localhost', 
#                               port=3306, 
#                               user='root', 
#                               password='sdkkxwban123', 
#                               db='liepin',
#                               auth_plugin='mysql_native_password')
#cursor = conn.cursor(buffered=True) # Locate the Cursor, all that was required was for buffered to be set to true
#
#sql="insert into job_info(URL,KEY_WORD,CITY,JOB_NAME,COMPANY,\
#SALARY,POSITION,JOB_QUALIFICATIONS,COM_TAG_LIST,CONTENT_WORD,\
#INFO_WORD,URL_COM,FIELD,COM_SIZE,LOCATION) \
#values(%s,%s,%s,%s,%s,\
#%s,%s,%s,%s,%s,\
#%s,%s,%s,%s,%s)"#,time_pub,%s,TIME_PUB
##values(%s,%s,%s,%s,%s)"
#ls1=(url,      key_word,city,              job_name,    company,#,)
#     salary,   position,job_qualifications,com_tag_list,content_word,
#     info_word,url_com, field,             com_size,    location)
#ls2=(url[:-1],      key_word,city,              job_name,    company,
#     salary,   position,job_qualifications,com_tag_list,content_word,
#     info_word,url_com, field,             com_size,    location)
##ls3=[7,'李3','女',15]
#ls=(ls1,ls2)
#cursor.executemany(sql,ls)
#
##提交更新
#conn.commit()
##关闭连接对象
#cursor.close()
#conn.close()
#
#    
##sql = "insert into job_info(URL,KEY_WORD,CITY,JOB_NAME,COMPANY)\
## values('%s','%s','%s','%s','%s')" % (url,      key_word,city,              job_name,    company)
##cursor.execute(sql)
##conn.commit()
##cursor.close()
##conn.close()
