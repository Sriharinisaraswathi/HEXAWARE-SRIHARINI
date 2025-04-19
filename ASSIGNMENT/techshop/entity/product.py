from exception.invalid_data_exception import InvalidDataException

class Product:
    def __init__(self, product_id, product_name, description, price):
        self._product_id = product_id
        self._product_name = product_name
        self._description = description
        self._price = price

    # Getters and Setters with validation
    @property
    def product_id(self):
        return self._product_id

    @property
    def product_name(self):
        return self._product_name

    @product_name.setter
    def product_name(self, value):
        if not value or not value.strip():
            raise InvalidDataException("Product name cannot be empty")
        self._product_name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not value:
            value = ""  # Description can be empty
        self._description = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise InvalidDataException("Price must be a non-negative number")
        self._price = value

    def get_product_details(self):
        return f"Product ID: {self._product_id}\nName: {self._product_name}\nDescription: {self._description}\nPrice: ₹{self._price:.2f}"

    def update_product_info(self, description=None, price=None):
        if description is not None:
            self.description = description
        if price is not None:
            self.price = price

    def is_product_in_stock(self, inventory):
        return inventory.get_quantity_in_stock(self._product_id) > 0