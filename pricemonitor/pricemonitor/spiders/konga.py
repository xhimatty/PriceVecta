import scrapy
import json
from datetime import datetime, timezone
from pricemonitor.items import PricemonitorItem

class KongaSpider(scrapy.Spider):
    name = "konga"
    allowed_domains = ["konga.com"]
    start_urls = [
        "https://www.konga.com/product/hp-elitebook-830-g7-touch-screen-intel-core-i7-512ssd-16gb-ram-backlit-keyboard-windows-11pro-6345188?cid=5253",
        "https://www.konga.com/product/binatone-electric-jug-cej-3000-3l-4037928",
        "https://www.konga.com/product/hisense-20l-microwave-mows14-6867788?cid=1212",
        "https://www.konga.com/product/mwkca-airf0601-air-fryer-6886244",
        "https://www.konga.com/product/samsung-galaxy-a06-6-7-128gb-rom-4gb-ram-4g-lte-dual-sim-fingerprint-5000mah-light-blue-6579675",
        "https://www.konga.com/product/silvercrest-extra-large-capacity-air-fryer-8l-2400w-5758080",
        "https://www.konga.com/product/silvercrest-extra-large-capacity-airfryer-6l-2400w-6726339",
    ]

    def parse(self, response):
        brand = None
        product = None
        price = None

        # 1. Parse structured LD+JSON schemas securely
        schemas = response.css('script[type="application/ld+json"]::text').getall()
        for schema_text in schemas:
            try:
                data = json.loads(schema_text)
                if data.get("@type") == "Product" or "Product" in str(data.get("@context", "")):
                    product = data.get("name")
                    
                    # Handle varying brand data nesting types securely
                    brand_data = data.get("brand")
                    if isinstance(brand_data, dict):
                        brand = brand_data.get("name")
                    else:
                        brand = brand_data
                    
                    # Handle offers data nesting securely
                    offers = data.get("offers", {})
                    if isinstance(offers, dict):
                        price = offers.get("price")
                    elif isinstance(offers, list) and offers:
                        price = offers[0].get("price")
                    break
            except Exception:
                continue

        # 2. Resilient fallback to traditional CSS selectors if schema metadata is missing
        if not product:
            product = response.css('h1::text, h2.product-name::text').get()
        if not price:
            raw_price = response.css('span.price::text, ._e24ff_3Vwdf::text').get()
            if raw_price:
                price = ''.join(c for c in raw_price if c.isdigit() or c == '.')

        # Validate that we extracted essential fields successfully
        if not product or price is None:
            self.logger.warning(f"Skipping page due to missing mandatory data: {response.url}")
            return

        # 3. Clean and cast values directly to match your SQLALchemy definitions
        item = PricemonitorItem()
        item['store'] = 'Konga'
        item['brand'] = str(brand).strip() if brand else "Generic"
        item['product'] = str(product).strip()
        
        try:
            item['price'] = float(price)
        except ValueError:
            self.logger.error(f"Could not convert price value '{price}' to float on page: {response.url}")
            return

        # Evaluate stock status seamlessly
        schema_avail = response.css('script[type="application/ld+json"]::text').re_first(r'"availability"\s*:\s*"([^"]+)"')
        item['availability'] = "In stock" if schema_avail and "InStock" in schema_avail else "Out of stock"
        
        item['url'] = response.url
        item['scraped_at'] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M %Z")

        yield item







    # def parse(self, response):
    #     json_text = response.css("script#__NEXT_DATA__::text").get()
    #     if json_text:
    #         data = json.loads(json_text)

    #         try:
    #             product_data = data["props"]["initialProps"]["pageProps"]["data"]["product"]

    #             brand = product_data.get('brand')
    #             product = product_data.get('name')
    #             price = product_data.get('price')

    #             if not product or not brand or price is None:
    #                 self.logger.warning(f"Skipping page due to missing mandatory data: {response.url}")
    #                 return

    #             item = PricemonitorItem()

    #             item['store'] = 'Konga'
    #             item['brand'] = brand.strip()
    #             item['product'] = product.strip()
    #             item['price'] = price

    #             schema_avail = response.css('script[type="application/ld+json"]::text').re_first(r'"availability"\s*:\s*"([^"]+)"')
    #             item['availability'] = "In stock" if schema_avail and "InStock" in schema_avail else "Out of stock"
    #             item['url'] = response.url
    #             item['scraped_at'] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M %Z")

    #             yield item

    #         except KeyError as e:
    #             self.logger.error(f"Data structure changed or missing key: {e}")
    #     else:
    #         self.logger.error("Could not find the __NEXT_DATA__ script tag on the page.")