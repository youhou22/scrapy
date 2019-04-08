# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from tianqi.items import TianqiItem


class TianqispiderSpider(scrapy.Spider):
    name = 'tianqispider'  # 爬虫名称
    allowed_domains = ['www.tianqihoubao.com']  # 规则域
    start_urls = ['http://www.tianqihoubao.com/lishi/weinan.html']  # 起始网址

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')  
        div = soup.find_all(name='div', class_='wdetail')
        lista = []
        for ul in div:
            for li in ul.find_all(name='div', class_='box pcity'):
                for a in li.find_all(name='a'):
                    lista.append(a['href'])

        urls = []
        for a in lista:
            a2 = a.split('/')
            urls.append(a2[-1])

        for url in urls:
            url = "http://www.tianqihoubao.com/lishi/weinan/month/" + url
            yield scrapy.Request(url=url, callback=self.parse_weather)


    def parse_weather(self, response):
        # 得到天气数据
        text = response.xpath("//table[@class='b']/tr/td/text()").extract()
        listall = []
        for t in text:
            t1 = t.replace(' ', '')
            t2 = t1.replace('\r', '')
            t3 = t2.replace('\n', '')
            if t3.strip() != '':
                listall.append(t3.strip())
        sublist = [listall[i:i + 3] for i in range(0, len(listall), 3)]
        # 得到具体日期数据
        date = response.xpath("//table[@class='b']/tr/td/a/text()").extract()
        listdate = []
        for d in date:
            d1 = d.replace(' ', '')
            d2 = d1.replace('\r', '')
            d3 = d2.replace('\n', '')
            if d3.strip() != '':
                listdate.append(d3.strip())
        # 将两者合二为一
        for i in range(0, len(listdate)):
            sublist[i].insert(0, listdate[i])
        # 将数据分为早上晚上
        for sub in sublist:
            sub2 = sub[1].split('/')
            sub3 = sub[2].split('/')
            sub4 = sub[3].split('/')
            sub.pop(1)
            sub.pop(1)
            sub.pop(1)
            sub.extend(sub2)
            sub.extend(sub3)
            sub.extend(sub4)
        for sub in sublist:
            item = TianqiItem()
            item['day'] = sub[0]
            item['weatherm'] = sub[1]
            item['weathern'] = sub[2]
            item['temm'] = sub[3]
            item['temn'] = sub[4]
            item['windm'] = sub[5]
            item['windn'] = sub[6]
            yield item



