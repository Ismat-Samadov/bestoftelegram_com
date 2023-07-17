import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class ChannelItem(scrapy.Item):
    channel_id = scrapy.Field()
    category = scrapy.Field()
    language = scrapy.Field()
    members = scrapy.Field()
    date_added = scrapy.Field()
    tags = scrapy.Field()

class TelegramSpider(scrapy.Spider):
    name = "main_scraper"
    allowed_domains = ["bestoftelegram.com"]
    start_urls = ["https://bestoftelegram.com/channels"]

    def parse(self, response):
        categories = response.xpath('/html/body/section[2]/div/div/div/div/a/@href').getall()
        for category in categories:
            category_url = response.urljoin(category)
            yield scrapy.Request(url=category_url,
                                 callback=self.parse_category,
                                 meta={'category': category})

    def parse_category(self, response):
        category = response.request.meta['category']
        yield from self.parse_page(response, category)

        next_page = response.css('div.pagination a.active + a::attr(href)').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse_category, meta={'category': category})

    def parse_page(self, response, category):
        channels = response.xpath('/html/body/section[2]/div/div/div/div/a[1]/@href').getall()
        for channel in channels:
            channel_url = response.urljoin(channel)
            yield scrapy.Request(url=channel_url,
                                 callback=self.parse_channel,
                                 meta={'category': category})

    def parse_channel(self, response):
        loader = ItemLoader(item=ChannelItem(), response=response)
        loader.default_output_processor = TakeFirst()

        loader.add_value('channel_id', response.xpath('//i[contains(@class, "icon-id-card-o")]/following-sibling::text()').get())
        loader.add_value('category', response.css('i.icon-filter + a::text').getall())
        loader.add_value('language', response.xpath('//i[contains(@class, "icon-language")]/following-sibling::text()').get())
        loader.add_value('members', response.xpath('//i[contains(@class, "icon-users")]/following-sibling::text()').get())
        loader.add_value('date_added', response.xpath('//i[contains(@class, "icon-clock")]/following-sibling::text()').get())
        loader.add_value('tags', response.css('div.reuse-inline-block a::text').getall())

        yield loader.load_item()
