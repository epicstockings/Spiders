# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 16:16:45 2018

@author: siwo
"""
import requests
import time
#from multiprocessing import Process
#from email_sender import error_sender,goodjob
def request_pic(url,savename):
    #aa=requests.request('http://baidu.com/robots.txt')
#    filename=url.split('/')[-1]
#    outpath=savepath+filename
    #try:
	kv0={'user-agent':'Mozilla/5.0'}
	r = requests.get(url,headers=kv0)
	r.status_code
	r.encoding = r.apparent_encoding
	with open(savename,'wb') as f:
		f.write(r.content)
    #except:
        #print('Error!')

if __name__=="__main__":
	try:
		savepath='/home/ubuntu/scrpy_nmc/weather_ana/'
		
		products=['L00','L92','L85','L70','L50','L20','L10']
		
		now=time.localtime(time.time()-8*3600)
		date=time.strftime("%Y/%m/%d",now)
		url_zero='http://image.nmc.cn/product/' + date + '/WESA/medium/'
		#地面的文件时间
		dateneed_d=time.strftime("%Y%m%d",now)+['0'+str(int(now.tm_hour/3)*3),
								str(int(now.tm_hour/3)*3)][int(now.tm_hour/3)*3 >= 10]
		#高空的文件时间
	#    dateneed_g=date+str(int(now.tm_hour/12)*12)
		if int(now.tm_hour/3) in [0,4]:
			filenames=[]
			for product in products:
				filename='SEVP_NMC_WESA_SFER_EGH_ACWP_' + product + '_P9_' + dateneed_d + '0000000.jpg'
				filenames.append(filename)
				savename=savepath + product + '/' + filename
				request_pic(url_zero + filename,savename)
			goodjob('pic_request',filenames)
		else:
			filename='SEVP_NMC_WESA_SFER_EGH_ACWP_' + 'L00' + '_P9_' + dateneed_d + '0000000.jpg'
			savename=savepath + 'L00' + '/' + filename
			#print(url_zero + filename)
			request_pic(url_zero + filename,savename)
			#goodjob('pic_request',[filename])
	except Exception as e:
		1
		#error_sender('pic_request',e)
		
		
