import scrapy

class TelegramSpider(scrapy.Spider):
    name = "category"
    allowed_domains = ["bestoftelegram.com"]
    start_urls = ["https://bestoftelegram.com/channels"]

    def parse(self, response):
        categories = response.xpath('/html/body/section[2]/div/div/div/div/a/@href').getall()
        for category in categories:
            yield response.follow(url=category,
                                  callback=self.parse_category,
                                  meta={'category': category})

    def parse_category(self, response):
        category = response.request.meta['category']
        channels = response.xpath('/html/body/section[2]/div/div/div/div/a[1]/@href').getall()
        for channel in channels:
            yield {
                "category": category,
                "channels": channel
            }

        next_page = response.xpath('//div[@class="pagination"]/a[@class="active"]/following-sibling::a[1]/@href').get()
