# -*- coding: utf-8 -*-
# Define your item pipelines here

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# ref to https://livedata.tistory.com/27?category=1026425
from __future__ import unicode_literals
from scrapy.exporters import JsonItemExporter, CsvItemExporter
import sys

class NewscrawlPipeline(object):
    def __init__(self):
        self.file = open("test.csv", 'wb')
        self.exporter = CsvItemExporter(self.file, encoding='utf-8')  # euc-kr할 필요없음 python3는 기본이 utf-8
        self.exporter.start_exporting()
 
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
         
    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()   #파일 CLOSE 