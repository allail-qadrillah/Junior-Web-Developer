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


#* Route endpoint displaying add profuct form
@main.route('/products/add', methods=['GET'])
def add_product_form():
    '''
    Render the template for adding a new product if the user has the required role.
    If the user is not authenticated or does not have the necessary role, redirect to the main index page.
    '''
    return render_template('add_product.html')

#* Route endpoint adding product
@main.route('/products/add', methods=['POST'])
def add_product():
    '''
    Add a new product to the database based on the form data received via POST request.
    Save the sales receipt file if provided and store its URL. Redirect to the products page after adding the product.
    
    Returns:
    Redirect to the products page after adding the product.
    '''
    # Get form data
    name = request.form['name']
    quantity = request.form['quantity']
    category = request.form['category']
    sell_price = request.form['sell_price']
    buy_price = request.form['buy_price']
    sales_receipt = request.files['sales_receipt']

    # Save sales receipt file and store its URL
    if sales_receipt:
        filename = secure_filename(sales_receipt.filename)
        upload_path = os.path.join('app/static/uploads', filename)
        sales_receipt.save(upload_path)
        sales_receipt_url = url_for('static', filename='uploads/' + filename)
    else:
        sales_receipt_url = None

    # Add product to the database
    DatabaseManager.add_product(
        name, category, quantity, sell_price, buy_price, sales_receipt_url)
    # Redirect to the products page
    return redirect(url_for('main.products'))

# * Route Generate weekly report
@main.route("/products/report")
def generate_report():
    """
    Generate a weekly report in PDF format containing information about products and items entered within the last week.
    The report includes details such as product name, category, prices, item ID, status, entry and exit dates.
    
    Returns the generated PDF file as an attachment for download.
    """
    # initialize start and end date for the last week
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=7)

    # Get products and items within the last week
    products = Product.query.all()
    items = Item.query.filter(
        Item.entry_date >= start_date, Item.entry_date <= end_date).all()

    # Create Path file PDF and SimpleDocTemplate
    pdf_path = os.path.join('app/static/reports', 'weekly_report.pdf')
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []

    # Header
    elements.append(Table([["Laporan Mingguan Produk dan Item"]], colWidths=[500]))
    elements.append(Table([[f"Periode: {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}"]], colWidths=[500]))

    # get data from products and items
    data = [["Produk", "Kategori", "Harga Jual", "Harga Beli", "Item ID", "Status", "Tanggal Masuk", "Tanggal Keluar"]]
    for product in products:
        for item in items:
            if item.product_id == product.product_id:
                data.append([
                    product.name, product.category, product.sell_price, product.buy_price,
                    item.item_id, item.status, item.entry_date, item.exit_date
                ])

    # create table and style
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
