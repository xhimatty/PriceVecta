from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class PriceMonitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(200), nullable=False)
    product = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    new_price = db.Column(db.Float)
    status = db.Column(db.String(200))
    availability = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(800), nullable=True)
    scraped_at = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))