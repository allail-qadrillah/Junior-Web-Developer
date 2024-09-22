from flask import (
    Blueprint, 
    render_template, 
    session, 
    redirect, 
    url_for,
    request, 
    send_file
)
from app.database import DatabaseManager
from app.models import Product, Item
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import os

# * Create a Blueprint for the main routes
main = Blueprint('main', __name__)

# * Route endpoint index
@main.route('/')
def index():
    return render_template('index.html')

# * Route endpoint display products
@main.route('/products')
def products():
    """
    Route to display products based on selected category or all categories.
    Fetches selected category from request args and retrieves all unique categories.
    Filters products by selected category or retrieves all products if no category selected.

    Returns:
    Renders products.html template with products, selected category, all categories, and user role.
    """
    # Get selected category from request args and all unique categories
    selected_category = request.args.get('category')
    all_category = [
        category[0] for category in Product.query.with_entities(Product.category).distinct().all()
    ]
   
    # Filter products by selected category or retrieve all products
    if selected_category:
        products = Product.query.filter_by(
            category=selected_category).all()
    else:
        products = DatabaseManager.get_all_products()

    # Render products.html template with products, selected category, all categories, and user role
    return render_template('products.html', 
                           products=products,
                           selected_category=selected_category,
                           all_category=all_category,
                           role=session['role'])

# * Route endpoint display items
@main.route('/products/<int:product_id>')
def items(product_id):
    '''
    Route to display items related to a specific product based on optional filters like status, start date, and end date.

    Parameters:
    - product_id (int): The unique identifier of the product to display items for.

    Returns:
    Rendered HTML template displaying items filtered by status, start date, and end date along with product details.
    '''
    # Get product details and optional filters from request args
    product = Product.query.get_or_404(product_id)
    status = request.args.get('status')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    query = Item.query.filter_by(product_id=product_id)

    # Filter items by status, start date, and end date
    if status:
        query = query.filter_by(status=status)
    if start_date:
        query = query.filter(Item.entry_date >= start_date)
    if end_date:
        query = query.filter(Item.entry_date <= end_date)

    # Retrieve items based on query filters
    items = query.all()

    

    # Render items.html template with product, items, selected status, start date, end date, and user role
    return render_template('items.html', 
                           product=product, 
                           items=items, 
                           selected_status=status, 
                           start_date=start_date, 
                           end_date=end_date,
                           role=session['role'])


# * Route Generate weekly report
@main.route("/products/report")
def generate_report():
    """
    Generate a weekly report in PDF format containing information about products and items entered within the last week.
    The report includes details such as product name, category, prices, item ID, status, entry and exit dates.
    
    Returns the generated PDF file as an attachment for download.
    """
    # initialize end date as today and start date as 3 months ago
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=90)

    # Get products and items within the last 3 months
    products = Product.query.all()
    items = Item.query.filter(
        Item.entry_date >= start_date, Item.entry_date <= end_date).all()

    # Create Path file PDF and SimpleDocTemplate
    pdf_path = os.path.join('app/static/reports', 'weekly_report.pdf')
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []

    # Header
    elements.append(
        Table([["Laporan Mingguan Produk dan Item"]], colWidths=[500]))

    # Group items by week
    grouped_items = {}
    for item in items:
        week_start = item.entry_date - \
            timedelta(days=item.entry_date.weekday())
        week_end = week_start + timedelta(days=6)
        week_key = (week_start.strftime('%Y-%m-%d'),
                    week_end.strftime('%Y-%m-%d'))
        if week_key not in grouped_items:
            grouped_items[week_key] = []
        grouped_items[week_key].append(item)

    # Create a table for each week
    for week, items in grouped_items.items():
        elements.append(
            Table([[f"Periode: {week[0]} - {week[1]}"]], colWidths=[500]))
        data = [["Produk", "Kategori", "Harga Jual", "Harga Beli",
                 "Item ID", "Status", "Tanggal Masuk", "Tanggal Keluar"]]
        for item in items:
            product = next(
                (p for p in products if p.product_id == item.product_id), None)
            if product:
                data.append([
                    product.name, product.category, product.sell_price, product.buy_price,
                    item.item_id, item.status, item.entry_date.strftime(
                        '%d-%B-%Y %H:%M'),
                    item.exit_date.strftime(
                        '%d-%B-%Y %H:%M') if item.exit_date else 'None'
                ])
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

    doc.build(elements)

    # Return the generated PDF file as an attachment for download
    return send_file("static/reports/weekly_report.pdf", as_attachment=True)
