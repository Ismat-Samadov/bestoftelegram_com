import scrapy


class ChannelsSpider(scrapy.Spider):
    name = "channels"
    allowed_domains = ["bestoftelegram.com"]
    start_urls = ["https://bestoftelegram.com/channels/entertainment?page=1"]

    def parse(self, response):
        channels_href = response.xpath('/html/body/section[2]/div/div/div/div/a[1]/@href').getall()
        for channel_href in channels_href:
            yield {
                'channel_href': channel_href
            }

        next_page = response.xpath('//div[@class="pagination"]/a[@class="active"]/following-sibling::a[1]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
