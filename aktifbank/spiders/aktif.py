import scrapy
from aktifbank.items import Article
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst


class AktifSpider(scrapy.Spider):
    name = 'aktif'
    allowed_domains = ['aktifbank.com.tr']
    start_urls = ['https://www.aktifbank.com.tr/en/about-us/press-room/news-from-us']

    def parse(self, response):
        year_links = response.xpath('//ul[@class="abcwmcn-years clearfix"]/li')
        for year_link in year_links:
            year = year_link.xpath('.//a/text()').get()
            link = year_link.xpath('.//a/@href').get()
            yield response.follow(link, self.parse_year, cb_kwargs=dict(year=year))

    def parse_year(self, response, year):
        article_links = response.xpath('//a[@class="abcwmcnlic-link"]/@href').getall()
        yield from response.follow_all(article_links, self.parse_article, cb_kwargs=dict(year=year))

    def parse_article(self, response, year):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//li[@id]/text()').get()
        content = response.xpath('//section[@class="abcwm-content"]//text()').getall()
        content = " ".join(content)

        item.add_value('title', title)
        item.add_value('date', year)
        item.add_value('link', response.url)
        item.add_value('content', content.strip())

        return item.load_item()

