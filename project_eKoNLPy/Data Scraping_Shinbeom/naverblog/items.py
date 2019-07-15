'''
입력 : 마라탕, 시작일자, 종료일자
출력 : 블로그 작성자, 제목, 작성일자, 내용
'''
import scrapy

### 데이터 정의서
### 결과 리턴할 때 형식 지정
### 이 형식 그대로 DB에 저장 가능

class MaratangItem(scrapy.Item):
    url = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    pass

class NewsCrawl(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    pass

class  NewscrawlItem(scrapy.Item):
    url =scrapy.Field()
    # author =scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pass

