# -*- coding: utf-8 -*-
import re
import scrapy
from newscrawl.items import NewscrawlItem
from datetime import timedelta, date
from urllib import parse
import time
import random
from time import sleep
# 2005.1 - 2017.12 이데일리 뉴스 가져오기
start_date = date(2018, 1, 1)
end_date = date(2018, 1, 2)
cnt_per_page = 10
keyword = "금리"
press_name = '이데일리'

url_format = ("https://search.naver.com/search.naver?where=news"+
    "&query={1}"+"&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=3"+
    "&ds={0}&de={0}"+"&docid=&nso=so:r,p:from{0}to{0},a:all&mynews=1"+
    "&cluster_rank=15&start={2}")

class NewscrawlSpider(scrapy.Spider):
    name = 'navercrawl'
    allowed_domains = ['naver.com','edaily.co.kr']
    start_urls = ['http://naver.com/']
    # 날짜 기간
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)
    
    # url_format에 date, keyword,start  저장
    for single_date in daterange(start_date, end_date):
        start_urls.append(url_format.format(single_date.strftime("%Y%m%d"), keyword, 1))

    # 들어갈 링크 접근
    def parse(self, response):
        for news in response.css('dl'):  
            title = news.css('dd span._sp_each_source::text').get()

            if title == press_name:
                link = news.css('dd a._sp_each_url::attr(href)').get()
                yield response.follow(link, self.parse_details)
            else:
                pass
        # for href in response.xpath("//li[contains(@id,'sp_nws')]/dl/dt/a/@href").extract():
        ## @href attr접근

        ### 전체 기사 건수 추출
        total_cnt = int(re.sub('[()전체건,]','',response.css('div.title_desc span::text').get().split('/')[1]))
        # re.sub(pattern, repl, string): string에서 pattern과 매치하는 텍스트를 repl로 치환한다
        ## []안에 들어가 있는 각 string 모두 치환.  # 1-10 / 36,631건
        query_str = parse.parse_qs(parse.urlsplit(response.url).query)
        currpage = int(query_str['start'][0])

        startdate = query_str['ds'][0]
        print("============== [" + startdate + '] ' + str(currpage) + 
        '/' + str(total_cnt) + "===============") 
        
        if currpage  < total_cnt :
            yield response.follow(url_format.format(startdate, keyword, currpage+10) , self.parse)

    def parse_details(self, response):    
        item = NewscrawlItem()
        
        try:  # 네이버 뉴스: 네이버부터 파싱해야 빠를 것
            item['url'] = response.url
            item['date'] = response.css('span.t11::text').get().split(' ')[0]
            # item['date'] = response.css('div.dates p:nth-child(1)::text').extract().split(' ')[1]
            # contains[string1, string2] : string1에 string2 가 포함되어 있는지 여부
            item['title'] = response.css('#articleTitle::text').get()
            item['content'] = response.css('#articleBodyContents::text').get()   # 일단 테스트로 첫문단만, getall하면 전부
            yield item

        except: # 이데일리 사이트
            item['url'] = response.url
            item['date'] = response.css('div.dates').xpath('//p[contains(text(),"등록")][1]/text()').get().split(' ')[1]
            # item['date'] = response.css('div.dates p:nth-child(1)::text').extract().split(' ')[1]
            # contains[string1, string2] : string1에 string2 가 포함되어 있는지 여부
            item['title'] = response.css('div.news_titles h2::text').get()
            item['content'] = response.css('div.news_body::text').get()   # 일단 테스트로 첫문단만, getall하면 전부
            yield item
        # 1달치 돌리는데 8분 걸림(본문 1문단씩만 가져옴.)-> 12년치 = 19시간?
        # 1달치 : 638개/31  = 1일당 약 20개 기사 -> 13년 = 94900개 기사
        
        ### 중간 중간에 1년치마다 csv로 저장하려면?

''' # 앞에 if문 다음에 들어감 - 관련뉴스까지 수집하기
           ##### 관련뉴스 수집하기 ####
            title2 = news.css('span.press::text').getall()
            if len(title2) > 0 :
                for idx, val in enumerate(title2):
                    if val == '연합인포맥스': 
                        link = news.css('ul.relation_lst li a::attr(href)').getall()
                        link = link[2*idx]
                        yield response.follow(link, self.parse_detail) 
                    else:
                        pass
            else:
                pass
'''