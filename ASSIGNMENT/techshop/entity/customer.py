import re
from exception.invalid_data_exception import InvalidDataException

class Customer:
    def __init__(self, customer_id, first_name, last_name, email, phone, address):
        self._customer_id = customer_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._phone = phone
        self._address = address
        self._orders = []  # Composition: Customer has Orders

    # Getters and Setters with validation
    @property
    def customer_id(self):
        return self._customer_id

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not value.strip():
            raise InvalidDataException("First name cannot be empty")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not value.strip():
            raise InvalidDataException("Last name cannot be empty")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise InvalidDataException("Invalid email format")
        self._email = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if not re.match(r"^\+?[0-9]{10,15}$", value):
            raise InvalidDataException("Invalid phone number format")
        self._phone = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not value or len(value.strip()) < 5:
            raise InvalidDataException("Address must be at least 5 characters")
        self._address = value

    @property
    def orders(self):
        return self._orders

    def calculate_total_orders(self):
        return len(self._orders)

    def get_customer_details(self):
        return f"Customer ID: {self._customer_id}\nName: {self._first_name} {self._last_name}\nEmail: {self._email}\nPhone: {self._phone}\nAddress: {self._address}\nTotal Orders: {self.calculate_total_orders()}"

    def update_customer_info(self, email=None, phone=None, address=None):
        if email:
            self.email = email
        if phone:
            self.phone = phone
        if address:
            self.address = address

    def add_order(self, order):
        self._orders.append(order)