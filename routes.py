from app import app
from flask import render_template, redirect, request, url_for, Response
from models import PriceMonitor, db
from sqlalchemy import or_
import csv
from io import StringIO
from werkzeug.utils import secure_filename



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    total_products = db.session.query(db.func.count(db.func.distinct(PriceMonitor.product))).scalar() or 0
    lowest_price = db.session.query(db.func.min(PriceMonitor.price)).scalar() or 0.0
    highest_price = db.session.query(db.func.max(PriceMonitor.price)).scalar() or 0.0
    time_recorded = db.session.query(db.func.max(PriceMonitor.scraped_at)).scalar()
    scraped_at = time_recorded.strftime('%Y-%m-%d %H:%M UTC') if time_recorded else "Never"
    
    query = request.args.get('query', '').strip()
    page = request.args.get('page', 1, type=int)
    results = PriceMonitor.query

    if query:
        results = results.filter(
            or_(
                PriceMonitor.store.ilike(f'%{query}%'),
                PriceMonitor.brand.ilike(f'%{query}%'),
                PriceMonitor.product.ilike(f'%{query}%'),
                PriceMonitor.status.ilike(f'%{query}%'),
                PriceMonitor.availability.ilike(f'%{query}%'),
            )
        )

    pagination = results.order_by(PriceMonitor.scraped_at.desc()).paginate(
        page=page,
        per_page=20,
        error_out=False
    )
    
    return render_template(
        'dashboard.html', 
        total_products=total_products,
        lowest_price=lowest_price,
        highest_price=highest_price,
        scraped_at=scraped_at,
        query=query,
        pagination=pagination
    )


@app.route('/history/<int:product_id>')
def history(product_id):
    clicked = PriceMonitor.query.get_or_404(product_id)

    records = PriceMonitor.query.filter_by(
        product=clicked.product,
        store=clicked.store
    ).order_by(PriceMonitor.scraped_at.desc()).all()

    return render_template(
        'history.html',
        records=records,
        product=clicked.product,
        store=clicked.store
    )

@app.route('/history/<int:product_id>/download')
def download_csv(product_id):
    clicked = PriceMonitor.query.get_or_404(product_id)

    records = PriceMonitor.query.filter_by(
        product=clicked.product,
        store=clicked.store
    ).order_by(PriceMonitor.scraped_at.desc()).all()

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Product', 'Price', 'New Price', 'Status', 'Date Tracked'])

    for record in records:
        cw.writerow([
            record.product,
            record.price,
            record.new_price,
            record.status,
            record.scraped_at.strftime('%Y-%m-%d %H:%M UTC')
        ])

    clean_name = secure_filename(clicked.product)
    filename = f"PriceVecta_History_{clean_name}.csv"
    response = Response(si.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response