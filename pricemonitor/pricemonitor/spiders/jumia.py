import scrapy
from pricemonitor.items import PricemonitorItem
from datetime import datetime, timezone


class JumiaSpider(scrapy.Spider):
    name = "jumia"
    allowed_domains = ["jumia.com.ng"]
    start_urls = [
        "https://www.jumia.com.ng/hp-elitebook-830-g7-touch-screen-intel-core-i7-512ssd16gb-ram-win-11-pro-186352094.html",
        "https://www.jumia.com.ng/binatone-3-litres-electric-jug-cej-3000-black-2-years-warranty-11450074.html",
        "https://www.jumia.com.ng/hisense-20-litres-microwave-h20mows14-white-with-1-year-warranty-400871962.html",
        "https://www.jumia.com.ng/mewe-6l-air-fryer-mwkca-airf0601-419234267.html",
        "https://www.jumia.com.ng/samsung-galaxy-a06-4gb-ram-128gb-rom-light-blue-380788785.html",
        "https://www.jumia.com.ng/silver-crest-8l-extra-large-digital-airfryer-418507707.html",
        "https://www.jumia.com.ng/silver-crest-6l-extra-large-capacity-digital-airfryer-310342956.html",
    ]

    def parse(self, response):
        item = PricemonitorItem()

        product = response.css('div.row.card h1::text').get()
        brand = response.css('div.row.card a._more::text').get()
        the_prie = response.css('div.row.card span.-b.-ubpt.-tal.-fs24.-prxs::text').get()
        price = the_prie.replace('₦','').replace(',','').strip() if the_prie else 0.0
        availability = response.css('div.row.card p.-df.-i-ctr.-fs12.-pbm::text').get()

        if not product or not brand:
            self.logger.warning(f"Skipping page due to missing required data on Jumia link: {response.url}")
            return

        
        item['store'] = 'Jumia'
        item['brand'] = brand.strip()
        item['product'] = product.strip()
        item['price'] = price
        item['availability'] = availability.strip() if availability else "In stock"
        item['url'] = response.url
        item['scraped_at'] = datetime.now(timezone.utc)

        yield item
