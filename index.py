#-*- coding: UTF-8 -*-
import sys
import os,shutil,platform,datetime
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import time
import base64

starttime = time.time()

domain = sys.argv[1]



filename = "cache/"+base64.encodestring(domain)+".html"
createFileTime = 0
if os.path.isfile(filename):
	createFileTime = os.path.getctime(filename)

#print starttime - createFileTime

if os.path.isfile(filename) and starttime - createFileTime < 3600.00:
    print open(filename, 'r').read()
else:
	s = get_project_settings()
	# s.update({
	#     'FEED_URI': 'quotes.csv',
	#     'LOG_FILE': 'quotes.log'
	# })
	proc = CrawlerProcess(s)


	#print domain
	proc.crawl("quotes",input='inputargument', domain=domain)
	proc.start()


endtime = time.time()
#print round(endtime - starttime,2) #执行时间







