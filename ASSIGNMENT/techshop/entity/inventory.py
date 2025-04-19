from datetime import datetime
from exception.insufficient_stock_exception import InsufficientStockException

class Inventory:
    def __init__(self, inventory_id, product, quantity_in_stock, last_stock_update=None):
        self._inventory_id = inventory_id
        self._product = product  # Composition
        self._quantity_in_stock = quantity_in_stock
        self._last_stock_update = last_stock_update or datetime.now()

    # Getters and Setters
    @property
    def inventory_id(self):
        return self._inventory_id

    @property
    def product(self):
        return self._product

    @property
    def quantity_in_stock(self):
        return self._quantity_in_stock

    @property
    def last_stock_update(self):
        return self._last_stock_update

    def get_product(self):
        return self._product

    def get_quantity_in_stock(self):
        return self._quantity_in_stock

    def add_to_inventory(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self._quantity_in_stock += quantity
        self._last_stock_update = datetime.now()

    def remove_from_inventory(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self._quantity_in_stock < quantity:
            raise InsufficientStockException(f"Only {self._quantity_in_stock} items available")
        self._quantity_in_stock -= quantity
        self._last_stock_update = datetime.now()

    def update_stock_quantity(self, new_quantity):
        if new_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        self._quantity_in_stock = new_quantity
        self._last_stock_update = datetime.now()

    def is_product_available(self, quantity_to_check):
        return self._quantity_in_stock >= quantity_to_check

    def get_inventory_value(self):
        return self._product.price * self._quantity_in_stock

    def is_low_stock(self, threshold):
        return self._quantity_in_stock < threshold

    def is_out_of_stock(self):
        return self._quantity_in_stock == 0