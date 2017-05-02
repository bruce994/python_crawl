#-*- coding: UTF-8 -*-
import scrapy
import base64
import re
import os,shutil,platform,datetime

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = "http://m.azhibo.com"

    def __init__(self, domain=None, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.start_urls = domain

    def start_requests(self):
        yield scrapy.Request(self.start_urls, callback=self.parse)

    def parse(self, response):
        body = response.body
        hxs = scrapy.Selector(response)
        #hxs = HtmlXPathSelector(response)

        config = open("config.txt", 'r')
        content = config.read()
        paths = content.split("\n") #split it into lines
        for path in paths:
            tmp =path.split(" = ")
            if len(tmp) > 1 :
                key = tmp[0]
                value = tmp[1]
                if key == "logo" :
                    body = body.replace("/images/new/logo.png",value)
                if key == "siteName" :
                    all_html = hxs.xpath('*//title/text()').extract()
                    all_html = set(all_html)
                    for html in all_html:
                        html = html.encode('utf-8')
                        body = body.replace(html,value)
                    body = body.replace("A直播",value)
                    body = body.replace("a直播",value)
                if key == "ad1" :
                    body = body.replace('<div class="row-fluid">','<div class="row-fluid">'+value)
                if key == "ad2" :
                    all_html = hxs.xpath('*//div[@class="bottom-footer"]').extract()
                    all_html = set(all_html)
                    for html in all_html:
                        html = html.encode("utf-8")
                        body = body.replace(html,value)


        #print 1111
        #exit()


        mapping = { 'target="_blank" >':'target="_blank">'}
        for k, v in mapping.iteritems():
            body = body.replace(k, v)


        all_html = hxs.xpath('*//div[@id="plugin-list"]').extract()
        all_html = set(all_html)
        for html in all_html:
            html = html.encode("utf-8")
            body = body.replace(html,"")
            #body = re.sub( html, '', body,re.S)



        all_html = hxs.xpath('*//a[@class="channel item"]').extract()
        all_html = set(all_html)
        for html in all_html:
            html = html.encode("utf-8")
            body = body.replace(html,"")


        all_html = hxs.xpath('*//div[@class="item download-app ad"]').extract()
        all_html = set(all_html)
        for html in all_html:
            html = html.encode("utf-8")
            body = body.replace(html,"")



        all_links = hxs.xpath('*//link/@href').extract()
        all_links = set(all_links)
        for link in all_links:
            link = link.decode().encode('utf-8')
            if link.find(self.allowed_domains) == -1 :
                body = body.replace(link,self.allowed_domains+link)

        all_img = hxs.xpath('*//img/@src').extract()
        all_img = set(all_img)
        for img in all_img:
            img = img.decode().encode('utf-8')
            if img.find(self.allowed_domains) == -1 and img.find("http://") == -1 and img.find("https://") == -1:
                body = body.replace(img,self.allowed_domains+img)


        all_html = hxs.xpath('*//script/@src').extract()
        all_html = set(all_html)
        for html in all_html:
            html = html.decode().encode('utf-8')
            if html.find(self.allowed_domains) == -1 and html.find("http://") == -1 :
                body = body.replace(html,self.allowed_domains+html)


        all_url = hxs.xpath("*//a/@href").extract()
        all_url = set(all_url)
        for a_url in all_url:
            a_url = a_url.decode().encode('utf-8')
            if a_url.find(self.allowed_domains) == -1 and a_url.find("http://") == -1 and a_url.find("https://") == -1 and len(a_url) > 3 :
                body = re.sub( r"\""+a_url+"\"", '"index.php?url='+base64.encodestring(self.allowed_domains+a_url)+'"', body,re.S)
                #body = body.replace(a_url,"index.php?url="+base64.encodestring(self.allowed_domains+a_url))



        all_url = hxs.xpath('*//div[@class="filter"]/a/@href').extract()
        all_url = set(all_url)
        for a_url in all_url:
            a_url = a_url.decode().encode('utf-8')
            body = re.sub( r"\""+a_url+"\"", '"index.php?url='+base64.encodestring(a_url)+'"', body,re.S)




        filename = "cache/"+base64.encodestring(self.start_urls)+".html"
        with open(filename, 'wb') as f:
            f.write(body)

        print body
