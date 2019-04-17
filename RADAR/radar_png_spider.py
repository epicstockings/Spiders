# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 18:11:58 2019

@author: siwo1
"""
#import datetime
import time
import requests
import os
import shutil
#下载图片
def get_png(time_UTC,filepath):
    #前20分钟最近的时间
    time_20 = time.localtime((time_UTC-20*60)-(time_UTC-20*60)%3600%360)
    time_30 = time.localtime((time_UTC-30*60)-(time_UTC-30*60)%3600%360)
    time_36 = time.localtime((time_UTC-36*60)-(time_UTC-36*60)%3600%360)
    regions = ['ANEC','ANCN','ASCN','ACCN','ANWC','ASWC','AECN']
    for region in regions:
        #拼接url
        url_0 = 'http://image.nmc.cn/product/'
        url_1 = '/RDCP/medium/'
        
        file_time = time.strftime('%Y%m%d%H%M',time_20)
        date  = time.strftime('%Y/%m/%d',time_20)
        filename_20 = 'SEVP_AOC_RDCP_SLDAS_EBREF_%s_L88_PI_%s00001.PNG'%(region,file_time)
        url = url_0 + date + url_1+ filename_20
        #请求url内容
        r = requests.get(url)
        with open(filepath + filename_20, 'wb') as f:
            #判断图片是否存在
            if len(r.content) > 20000: 
                #存储
                f.write(r.content)
        #判断30分钟前的文件是否存在,存在则跳过，不存在则用前6分钟的替代
        filename_30 = 'SEVP_AOC_RDCP_SLDAS_EBREF_%s_L88_PI_%s00001.PNG'%(region,time.strftime('%Y%m%d%H%M',time_30))
        filename_36 = 'SEVP_AOC_RDCP_SLDAS_EBREF_%s_L88_PI_%s00001.PNG'%(region,time.strftime('%Y%m%d%H%M',time_36))
        if os.path.exists(filepath + filename_30):
            continue
        else:
            try:
                shutil.copy(filepath + filename_36, filepath + filename_30)
            except:
                continue

if __name__ == '__main__':
    time_UTC = time.time()-8*3600
    dirpath = ''
    get_png(time_UTC,dirpath)
