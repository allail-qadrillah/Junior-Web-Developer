from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
)
from werkzeug.utils import secure_filename
from app.database import DatabaseManager
import os

form = Blueprint('form', __name__)

# * Route endpoint add product form
@form.route('/product/add', methods=['GET'])
def add_product():
    '''
    Route to add a new product to the database if the request method is POST. 
    Retrieves product details from the form data, saves the sales receipt file, 
    and adds the product to the database. Redirects to the products page after adding the product. 

    Returns: 
    - Redirect to the products page after adding the product.
    - Renders the 'add_product.html' template if the request method is GET
    '''
    # 
    if request.method == 'POST':
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

        # Add product to the database and redirect to the products page
        DatabaseManager.add_product(
            name, category, quantity, sell_price, buy_price, sales_receipt_url)
        return redirect(url_for('main.products'))
    
    # Render the 'add_product.html' template if the request method is GET
    return render_template('add_product.html')


# * Route endpoint reduce product
@form.route('/product/reduce', methods=['GET', 'POST'])
def reduce_product():
    '''
    Route to reduce the quantity of a product in the database. Handles both GET and POST requests. 
    If a POST request is received, updates the item quantity, status, and purchase receipt in the database. 
    If the status is 'sold' and a purchase receipt is provided, saves the receipt file and updates the database. 
    
    Returns:
    - Redirects to the products page after processing the request. 
    - If a GET request is received, retrieves all products from the database and renders the 'reduce_product.html' template.
    '''
    if request.method == 'POST':
        # Get form data
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])
        status = request.form['status']
        purchase_receipt = request.files.get('purchase_receipt')

        # Save purchase receipt file and store its URL
        if status == 'sold' and purchase_receipt:
            filename = secure_filename(purchase_receipt.filename)
            upload_path = os.path.join('app/static/uploads', filename)
            purchase_receipt.save(upload_path)
            purchase_receipt_url = url_for(
                'static', filename='uploads/' + filename)
        else:
            purchase_receipt_url = None

        # Reduce item quantity in the database and redirect to the products page
        DatabaseManager.reduce_item_quantity(
            product_id, quantity, status, purchase_receipt_url)
        return redirect(url_for('main.products'))

    # Retrieve all products from the database and render the 'reduce_product.html' template
    products = DatabaseManager.get_all_products()
    return render_template('reduce_product.html', products=products)


# * Route endpoint handle edit product
@form.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    """
    Edit a product based on the provided product ID.

    Parameters:
    - product_id (int): The ID of the product to be edited.

    Returns:
    - Redirects to the products page after editing the product.
    - Renders the 'edit_product.html' template with the product details.
    """
    # Get the product details from the database
    product = DatabaseManager.get_product_by_id(product_id)
    if not product:
        return redirect(url_for('main.products'))

    # Update the product details in the database
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        sell_price = request.form['sell_price']
        buy_price = request.form['buy_price']

        DatabaseManager.update_product(product_id, name=name, category=category, sell_price=sell_price, buy_price=buy_price)
        return redirect(url_for('main.products'))

    # Render the 'edit_product.html' template with the product details
    return render_template('edit_product.html', product=product)


# * Route handle Delete Product
@form.route('/product/delete/<int:product_id>')
def delete_product(product_id):
    """
    Delete a product from the database based on the provided product_id.

    Parameters:
    - product_id (int): The unique identifier of the product to be deleted.

    Returns:
    Redirects to the 'main.products' route after deleting the product.
    """
    # Get the product details from the database
    product = DatabaseManager.get_product_by_id(product_id)

    # Delete the product from the database
    if product:
        DatabaseManager.delete_product(product_id)

    # Redirect to the products page
    return redirect(url_for('main.products'))
