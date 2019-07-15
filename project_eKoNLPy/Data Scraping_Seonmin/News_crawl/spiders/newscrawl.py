# -*- coding: utf-8 -*-

# 과거 뉴스 크롤러(네이버 뉴스를 통해 크롤링하기)
# keyword와 날짜 그리고 if문에서 언론사명만 바꿔주면 원하는 언론사 크롤링 가능

# 2005 ~ 2011까지의 연합인포맥스 뉴스 가져오기
# 네이버 뉴스에서 기간 짧게(하루-이틀정도) 설정하고 나오는 뉴스 목록 중
# 언론사명이 '연합인포맥스'인 경우 링크 타고 들어가고
# 그 뉴스 상세 페이지에서 원하는 내용 크롤링하기
# 날짜 짧게 설정해서 request 날리는것 필요함. 

# span._sp_each_source 또는 span.press 에서 '연합인포맥스'일 경우 가져온다.
# span.press는 줄기가 아니라 밑에 딸린 가지 뉴스임 -> 관련뉴스

import scrapy
import re
from datetime import timedelta, date
from urllib import parse
import time
import random
from time import sleep
# https://search.naver.com/search.naver?
# &where=news
# &query=%EA%B8%88%EB%A6%AC
# &nso=so:r,p:from20050101to20050102,a:all
# &start=1

start_date = date(2005, 1, 1)
end_date = date(2011, 2, 28)
cnt_per_page = 10
keyword = "금리"
url_format = 'https://search.naver.com/search.naver?&where=news&query={0}&start={1}&nso=so:r,p:from{2}to{2},a:all'



item = {}
class NewscrawlSpider(scrapy.Spider):
    def date_range(start_date, end_date):
        for i in range(int ((end_date - start_date).days)+1):
            yield start_date + timedelta(i)

    name = 'newscrawl'
    start_urls = []

    for single_date in date_range(start_date, end_date):
        start_urls.append(url_format.format(keyword,1,single_date.strftime('%Y%m%d')))
        

    # allowed_domains = ['naver.com']
    def parse(self, response):
        for news in response.css('dl'):  
            title = news.css('dd span._sp_each_source::text').get()

            if title == '연합인포맥스':
                link = news.css('dd a._sp_each_url::attr(href)').get()

                yield response.follow(link, self.parse_detail)
            else:
                pass

            ############################
            ##### 관련뉴스 수집하기 #####
            ############################
            title2 = news.css('span.press::text').getall()

            if len(title2) > 0 :
                for idx, val in enumerate(title2):
                    if val == '연합인포맥스': 
                        link = news.css('ul.relation_lst li a::attr(href)').getall()
                        # print('***************************', link)
                        link = link[2*idx]
                        yield response.follow(link, self.parse_detail) 
                    else:
                        pass
            else:
                pass

        total_cnt = int(re.sub('건', '', response.css('div.title_desc.all_my span::text').get().split('/')[1])) 
        query_str = parse.parse_qs(parse.urlsplit(response.url).query)   # url에서 query 분해해서 저장하는 변수
        currpage = int(query_str['start'][0])
    

        startdate = query_str['nso'][0]
        print("=================== [" + startdate + '] ' + str(currpage) + '/' + str(total_cnt) + "===================") 
        ################################################
        ###########    TIME ############################
        ################################################
        sleep(0.5)
        ################################################
        ################################################
        if currpage  < total_cnt : 
            yield response.follow(url_format.format(keyword, currpage+10, startdate) , self.parse)
            

    def parse_detail(self, response):
        table = response.css('div.content')
        
        press = table.css('div.press_logo a img::attr(title)').get()
        title = table.css('h3::text').get()
        date = table.css('span.t11::text').get().split(' ')[0].replace('.','')
        link = response.url
        content = str(table.xpath('//div[@id="articleBodyContents"]/text()').getall())
        content = re.sub(' +', ' ', str(re.sub(re.compile('<.*?>'), ' ', content.replace('"','')).replace('\r\n','').replace('\n','').replace('\t','').replace('\u200b','').replace('\\n\\t','').replace('\\n\\n','').replace('\\n','').replace('\\n\\t\\n\\t','').replace('\\n\\n\\t','').replace(' ','').strip()))
        

        item['press'] = press
        item['date'] = date
        item['title'] = title 
        item['link'] = link
        item['content'] = content

        yield item
        
