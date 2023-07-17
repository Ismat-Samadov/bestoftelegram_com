import scrapy


class ChannelSpider(scrapy.Spider):
    name = "channel"
    allowed_domains = ["bestoftelegram.com"]
    start_urls = ["https://bestoftelegram.com/channels/CryptoMemesHub"]

    def parse(self, response):
        channel_data = response.xpath('/html/body/section[1]/div[1]/div[2]/div[2]/div[1]/p/text()').getall()
        yield {
            "channel_data": channel_data
        }

