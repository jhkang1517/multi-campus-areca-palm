# -*- coding: utf-8 -*-
# Define here the models for your scraped items
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
### 결과 리턴할 때 형식 지정
### 이 형식 그대로 DB에 저장 가능

class  NewscrawlItem(scrapy.Item):
    # press = scrapy.Field()
    url =scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pass