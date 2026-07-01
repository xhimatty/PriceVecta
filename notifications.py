import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()


TELEGRAM_TOKEN = os.getenv("PRICEVECTA_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("PRICEVECTA_CHAT_ID")

logging.basicConfig(
    level=logging.INFO,
    filename="notifications.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
)
logger = logging.getLogger("notification")


def send_alert(event_type, product_name, old_price=None, new_price=None, url=None):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.error('Telegram credentials missing from .env file.')
        return
    
    if event_type ==  'Price Drop':
        message = (
            f"📉 <b>Price Drop!</b>\n"
            f"Product: {product_name}\n"
            f"Old Price: ₦{old_price:,.2f}\n"
            f"New Price: ₦{new_price:,.2f} 🎉\n"
            f"<a href='{url}'>View Product</a>"
        )

    elif event_type == 'Price Increase':
        message = (
            f"📈 <b>Price Increase!</b>\n"
            f"Product: {product_name}\n"
            f"Old Price: ₦{old_price:,.2f}\n"
            f"New Price: ₦{new_price:,.2f}\n"
            f"<a href='{url}'>View Product</a>"
        )

    else:
        logger.warning(f"Unknown event_type: {event_type}")
        return

    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }        

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Alert sent: {event_type} - {product_name}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram alert: {e}")