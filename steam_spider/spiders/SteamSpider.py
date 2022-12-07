import scrapy
import requests
import lxml.html as html
from ..items import SteamSpiderItem
import re


class SteamSpider(scrapy.Spider):
    name = 'SteamSpider'

    def get_query_urls(self):
        urls = [f'https://store.steampowered.com/search/?sort_by=&sort_order=0&term={self.query1}&page=1',
                f'https://store.steampowered.com/search/?sort_by=&sort_order=0&term={self.query1}&page=2',
                f'https://store.steampowered.com/search/?sort_by=&sort_order=0&term={self.query2}&page=1',
                f'https://store.steampowered.com/search/?sort_by=&sort_order=0&term={self.query2}&page=2',
                f'https://store.steampowered.com/search/?sort_by=&sort_order=0&term={self.query3}&page=1',
                f'https://store.steampowered.com/search/?sort_by=&sort_order=0&term={self.query3}&page=2']
        return urls

    def start_requests(self):
        urls = self.get_query_urls()
        for url in urls:
            r = requests.get(url)
            page = r.content.decode('utf-8')
            response = html.document_fromstring(page)
            start_urls = response.xpath('//span[@class="title"]/ancestor::a/@href')
            for start_url in start_urls:
                yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        if 'agecheck' in response.url:
            return

        game = SteamSpiderItem()

        try:
            name = response.xpath('//span[@itemprop="name"]/text()').extract()[0]
        except IndexError:
            return

        category = response.xpath('//div[@class="blockbg"]//text()').extract()[3:-3:2]

        try:
            reviews_amount = response.xpath(
                '//div[@class="subtitle column all"]/following-sibling::div[1]/span[@class="responsive_hidden"]/text()').extract()[
                0]
            reviews_amount = re.findall(r'\d+', reviews_amount)[0]
            general_score = response.xpath(
                '//div[@class="subtitle column all"]/following-sibling::div[1]/span[@itemprop="description"]/text()').extract()[
                0]
        except IndexError:
            reviews_amount = 'No user reviews'
            general_score = 'No user reviews'

        try:
            release_date = response.xpath('//div[@class="date"]/text()').extract()[0]
        except IndexError:
            release_date = 'Unknown'

        developer = response.xpath('//div[text()="Developer"]/following-sibling::div[1]/a/text()').extract()[0]

        tags = response.xpath(
            '//div[text()="Popular user-defined tags for this product:"]/following-sibling::div[1]/a/text()').extract()  # как по-другому?
        tags = list(map(lambda tag: re.sub(r'[\n\r\t]', r'', tag), tags))

        price = response.xpath('//div[@class="game_purchase_price price"]/text()').extract()
        if len(price) == 0:
            price = response.xpath('//div[@class="discount_final_price"]/text()').extract()
        try:
            price = re.sub(r'[\n\r\t]', r'', price[0])
        except IndexError:
            price = 'Unknown'

        platforms_dict = {"platform_img win": "Windows",
                          "platform_img linux": "Linux",
                          "platform_img mac": "MacOS",
                          "vr_supported": "VR",
                          "platform_img music": "Music",
                          "vr_required": "VR"}

        platforms = list(set(response.xpath('//div[@class="game_area_purchase_platform"]/span/@class').extract()))
        platforms = list(map(lambda platform: platforms_dict[platform], platforms))
        if len(platforms) == 0:
            platforms = 'Unknown'
        else:
            platforms = ', '.join(platforms)

        game['name'] = name
        game['category'] = '/'.join(category)
        game['reviews_amount'] = reviews_amount
        game['general_score'] = general_score
        game['release_date'] = release_date
        game['developer'] = developer
        game['tags'] = ', '.join(tags)
        game['price'] = price
        game['platforms'] = platforms
        return game
