from app import db
from .models import Product, Item
from datetime import datetime

class DatabaseManager:
    """
    DatabaseManager class for managing products and items in the database.

    Methods:
        add_product: Add a new product or update an existing one with items.
        get_all_products: Retrieve all products from the database.
        get_product_by_id: Get a product by its ID.
        update_product: Update details of a product.
        delete_product: Delete a product and its associated items.
        reduce_item_quantity: Reduce the quantity of available items for a product.
    """
    @staticmethod
    def add_product(name: str, category: str, quantity: int, sell_price: float, buy_price: float, sales_receipt: str):
        '''
        Add a new product or update an existing one with items.

        Parameters:
            name (str): The name of the product.
            category (str): The category of the product.
            quantity (int): The quantity of items to add.
            sell_price (float): The selling price of the product.
            buy_price (float): The buying price of the product.
            sales_receipt (str): The sales receipt associated with the item.

        Returns:
            Product: The existing product if updated, or the new product added with items.
        '''
        # check if the product already exists
        existing_product = Product.query.filter_by(
            name=name, category=category, sell_price=sell_price, buy_price=buy_price).first()

        # if the product already exists, add the quantity to the existing product
        if existing_product:
            for _ in range(int(quantity)):
                new_item = Item(product_id=existing_product.product_id,
                                status='available', sales_receipt=sales_receipt)
                db.session.add(new_item)
        # if the product does not exist, create a new product
        else:
            new_product = Product(
                name=name, category=category, sell_price=sell_price, buy_price=buy_price)
            db.session.add(new_product)
            db.session.commit()
            
            # add item for the new product based on the quantity
            for _ in range(int(quantity)):
                new_item = Item(product_id=new_product.product_id,
                                status='available', sales_receipt=sales_receipt)
                db.session.add(new_item)

        # commit the changes to the database
        db.session.commit()
        return existing_product if existing_product else new_product

    @staticmethod
    def get_all_products():
        '''
        Retrieve all products from the database.

        Returns:
            list: A list of all products in the database.
        '''
        return Product.query.all()

    @staticmethod
    def get_product_by_id(product_id:int):
        '''
        Get a product by its ID.

        Parameters:
            product_id (int): The unique identifier of the product.

        Returns:
            Product: The product corresponding to the provided ID.
        '''
        return Product.query.get(product_id)

    @staticmethod
    def update_product(product_id:int, name:str=None, category:str=None, sell_price:float=None, buy_price:float=None):
        '''
        Update details of a product.

        Parameters:
            product_id (int): The unique identifier of the product.
            name (str): The new name of the product (optional).
            category (str): The new category of the product (optional).
            sell_price (float): The new selling price of the product (optional).
            buy_price (float): The new buying price of the product (optional).

        Returns:
            Product: The updated product object if successful, otherwise None.
        '''
        product = Product.query.get(product_id)

        # if the product exists, update the details
        if product:
            if name:
                product.name = name
            if category:
                product.category = category
            if sell_price:
                product.sell_price = sell_price
            if buy_price:
                product.buy_price = buy_price
            db.session.commit()
        return product

    @staticmethod
    def delete_product(product_id:int):
        '''
        Delete a product and its associated items from the database.

        Parameters:
            product_id (int): The unique identifier of the product to be deleted.

        Returns:
            bool: True if the product and its items are successfully deleted, False otherwise.
        '''
        product = Product.query.get(product_id)

        # if the product exists, delete the product and its items
        if product:
            items = Item.query.filter_by(product_id=product_id).all()
            
            # delete each item associated with the product
            for item in items:
                db.session.delete(item)
            db.session.delete(product)
            db.session.commit()
            return True
        return False

    @staticmethod
    def reduce_item_quantity(product_id:int, quantity:int, status:str, purchase_receipt:str=None):
        '''
        Reduce the quantity of available items for a product.

        Parameters:
            product_id: The identifier of the product.
            quantity: The number of items to reduce.
            status: The new status for the items.
            purchase_receipt: The purchase receipt associated with the items (optional).

        '''
        items = Item.query.filter_by(product_id=product_id, status='available').limit(quantity).all()
        for item in items:
            item.status = status
            item.exit_date = datetime.utcnow()
            if status == 'sold':
                item.purchase_receipt = purchase_receipt
        db.session.commit()
