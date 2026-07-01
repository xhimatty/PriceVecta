import scrapy
from pricemonitor.items import PricemonitorItem
from datetime import datetime, timezone


class SolatonlineSpider(scrapy.Spider):
    name = "solatonline"
    allowed_domains = ["solatonline.ng"]
    start_urls = [
        "https://www.solatonline.ng/product/hisense-20l-convection-microwave-oven/",
        "https://www.solatonline.ng/product/mewe-air-fryer-mwkca-airfo601/",
    ]

    def parse(self, response):
        item = PricemonitorItem()

        card = response.css('div.mf-product-detail')
        product = card.css('h1.product_title::text').get()
        brand = card.css('li.meta-brand a.meta-value::text').get()
        the_price =  card.css('p.price bdi::text').getall()[-1]
        price = the_price.replace(',','').strip() if the_price else 0.0
        availability = card.css('p.stock.in-stock::text').getall()[-1].strip()

        if not product or not brand:
            self.logger.warning(f"Skipping page due to missing required data on Solatonline link: {response.url}")
            return
        

        item['store'] = 'Solatonline'
        item['brand'] = brand.strip()
        item['product'] = product.strip()
        item['price'] = price
        item['availability'] = availability.strip() if availability else "In stock"
        item['url'] = response.url
        item['scraped_at'] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M %Z")

        yield item