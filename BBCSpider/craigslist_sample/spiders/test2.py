from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from craigslist_sample.items import BBCItem
import scrapy
import re
import os.path
from scrapy.utils.response import body_or_str

class MySpider(CrawlSpider):
    name = "bbc"
    allowed_domains = ["bbc.com"]
    start_urls = ["http://www.bbc.com"]

    rules = (
        Rule(LinkExtractor(allow=('news/')), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        items = []
        item = BBCItem()
        item["title"] = hxs.select('//h1[@class="story-body__h1"]/text()').extract()
        item["article"] = hxs.select('//div[@class="story-body__inner"]/p/text()').extract()
        item["link"] = response.url
        item["date"] = hxs.select('//div[@class="date date--v2"]/text()').extract()[0]
        items.append(item)
        return(items)