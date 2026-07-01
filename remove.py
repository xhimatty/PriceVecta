# from app import app
# from models import db, PriceMonitor

# with app.app_context():
#     # 1. Look at what is actually causing the block for your test items
#     # Let's delete the records created TODAY for those specific products to roll back the clock cleanly
#     from datetime import datetime, date
    
#     # This deletes ONLY records from today so you don't lose old dashboard history
#     deleted = PriceMonitor.query.filter(
#         PriceMonitor.scraped_at >= datetime.combine(date.today(), datetime.min.time())
#     ).delete()
    
#     db.session.commit()
#     print(f"Cleaned up {deleted} recent records from today. The timeline is rolled back safely.")