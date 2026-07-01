# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
from datetime import datetime, timezone
from models import db, PriceMonitor
from app import app
from notifications import send_alert


class PricemonitorPipeline:
    def process_item(self, item, spider):
        with app.app_context():
            last_record = PriceMonitor.query.filter_by(
            store=item["store"], product=item["product"]
            ).order_by(PriceMonitor.scraped_at.desc()).first()

            incoming_price = float(item['price'])
            
            if last_record:
                previous_price = last_record.new_price
            else:
                previous_price = incoming_price

            prices = pd.Series([previous_price, incoming_price], index=['price', 'new_price'])
            if prices['new_price'] > prices['price']:
                the_status = 'Price Increase'
            elif prices['new_price'] < prices['price']:
                the_status = 'Price Drop'
            else:
                the_status = 'No Change'

            new_record = PriceMonitor(
                store=item["store"],
                brand=item["brand"],
                product=item["product"],
                price=previous_price,
                new_price=incoming_price,
                status=the_status,
                availability=item["availability"],
                url=item["url"],
                scraped_at=datetime.now(timezone.utc),
            )

            db.session.add(new_record)
            try:
                db.session.commit()
                spider.logger.info(f"Successfully logged {item['product']} ({the_status})")

            except Exception as e:
                db.session.rollback()
                spider.logger.error(f"Database save failed: {e}")

            if the_status in ('Price Drop', 'Price Increase'):
                send_alert(
                    event_type=the_status,
                    product_name=item["product"],
                    old_price=previous_price,
                    new_price=incoming_price,
                    url=item["url"]
                )

        return item
