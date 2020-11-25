# -*- coding: utf-8 -*-
from manager.engine import Spider
import scrapy

from spider_code.items import AutoItem


class ExampleSpider(Spider):
    name = 'example'
    priority_queue = True  # 开启优先级队列

    def __init__(self, *args, **kwargs):
        super(ExampleSpider, self).__init__(*args, **kwargs)
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',}

    def start_requests(self):
        url = "https://www.baidu.com"
        yield scrapy.Request(
            url=url,
            headers=self.header,
            priority=1
        )

    def parse(self, response):
        news_li = response.xpath("//ul[@class='s-hotsearch-content']/li")
        for news in news_li:
            title = news.xpath("string(./a)").extract_first("").strip()
            url = news.xpath("./a/@href").extract_first()
            yield scrapy.Request(
                url=url,
                headers=self.header,
                callback=self.parse_news,
                meta={'title': title},
                priority=2
            )

    def parse_news(self, response):
        content = response.text.strip()
        item = AutoItem()
        item['title'] = response.meta['title']
        item['content'] = content
        item['url'] = response.url
        yield item


if __name__ == '__main__':
    from manager.run import run

    run(["example", "example", "auto", 1])  # 生产加消费
    # run(["example", "example", "m", 1])  # 生产
    # run(["example", "example", "w", 1])  # 消费
