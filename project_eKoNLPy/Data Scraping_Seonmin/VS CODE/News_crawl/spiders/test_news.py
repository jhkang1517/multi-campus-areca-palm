# -*- coding: utf-8 -*-
import scrapy


class TestNewsSpider(scrapy.Spider):
    name = 'test_news'
    allowed_domains = ['naver.com']
    start_urls = ['https://search.naver.com/search.naver?where=news&query=%EA%B8%88%EB%A6%AC&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds=2005.01.03&de=2005.01.03&docid=&nso=so%3Ar%2Cp%3Afrom20050103to20050103%2Ca%3Aall&mynews=0&refresh_start=0&related=0']

    def parse(self, response):
        count = response.css('div.title_desc.all_my span::text').get()
        print('*************************')
        print(count)
        
