from exception.insufficient_stock_exception import InsufficientStockException

class OrderDetail:
    def __init__(self, order_detail_id, order, product, quantity):
        self._order_detail_id = order_detail_id
        self._order = order  # Composition
        self._product = product  # Composition
        self._quantity = quantity

    # Getters and Setters with validation
    @property
    def order_detail_id(self):
        return self._order_detail_id

    @property
    def order(self):
        return self._order

    @property
    def product(self):
        return self._product

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Quantity must be a positive integer")
        self._quantity = value

    def calculate_subtotal(self):
        return self._product.price * self._quantity

    def get_order_detail_info(self):
        return f"{self._product.product_name} x {self._quantity} = ₹{self.calculate_subtotal():.2f}"

    def update_quantity(self, new_quantity, inventory):
        if new_quantity < self._quantity:
            # Reducing quantity - add back to inventory
            diff = self._quantity - new_quantity
            inventory.add_to_inventory(self._product.product_id, diff)
        else:
            # Increasing quantity - check stock first
            diff = new_quantity - self._quantity
            if inventory.get_quantity_in_stock(self._product.product_id) < diff:
                raise InsufficientStockException("Not enough stock available")
            inventory.remove_from_inventory(self._product.product_id, diff)
        
        self._quantity = new_quantity

    def add_discount(self, discount_percentage):
        if not 0 <= discount_percentage <= 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        discounted_price = self._product.price * (1 - discount_percentage / 100)
        self._product.price = discounted_price