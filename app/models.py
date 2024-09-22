from app import db
from datetime import datetime

class Product(db.Model):
    """
    Object representing a product in the database.

    Attributes:
        product_id (int): The unique identifier for the product.
        name (str): The name of the product.
        category (str): The category of the product.
        sell_price (float): The selling price of the product.
        buy_price (float): The buying price of the product.

    Methods:
        __repr__: Returns a string representation of the product.
        item_count: Calculates and returns the count of `available` items for this product.
    """
    # Define the columns of the 'product' table
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Text)
    sell_price = db.Column(db.Float, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        '''Returns a string representation of the product.'''
        return f'<Product {self.name}>'

    @property
    def item_count(self):
        '''Calculates and returns the count of `available` items for this product.'''
        total_items = 0
        for item in self.items:
            if item.status == 'available':
                total_items += 1    
        return total_items

class Item(db.Model):
    """
    Object representing an item in the database.

    Attributes:
        item_id (int): The unique identifier for the item.
        product_id (int): The identifier of the associated product.
        entry_date (datetime): The date and time when the item was entered.
        exit_date (datetime): The date and time when the item was exited, if applicable.
        status (str): The status of the item.
        sales_receipt (str): The sales receipt associated with the item.
        purchase_receipt (str): The purchase receipt associated with the item.
        product (relationship): Relationship to the associated Product model.

    Methods:
        __repr__: Returns a string representation of the item.
    """
    # Define the columns of the 'item' table
    item_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)
    exit_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(100), nullable=False)
    sales_receipt = db.Column(db.String(100), nullable=True)
    purchase_receipt = db.Column(db.String(100), nullable=True)

    # Define the relationship between the 'item' and 'product' tables
    product = db.relationship('Product', backref=db.backref('items', lazy=True))

    def __repr__(self):
        '''Returns a string representation of the Item.'''
        return f'<Item {self.item_id} of Product {self.product.name}>'
