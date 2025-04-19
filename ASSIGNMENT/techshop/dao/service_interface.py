from abc import ABC, abstractmethod
from entity.customer import Customer
from entity.product import Product
from entity.order import Order
from entity.order_detail import OrderDetail
from entity.inventory import Inventory

class TechShopService(ABC):
    # Customer operations
    @abstractmethod
    def get_all_customers(self):
        pass

    @abstractmethod
    def get_customer_by_id(self, customer_id):
        pass

    @abstractmethod
    def add_customer(self, customer):
        pass

    @abstractmethod
    def update_customer(self, customer):
        pass

    @abstractmethod
    def delete_customer(self, customer_id):
        pass

    # Product operations
    @abstractmethod
    def get_all_products(self):
        pass

    @abstractmethod
    def get_product_by_id(self, product_id):
        pass

    @abstractmethod
    def add_product(self, product):
        pass

    @abstractmethod
    def update_product(self, product):
        pass

    @abstractmethod
    def delete_product(self, product_id):
        pass

    # Order operations
    @abstractmethod
    def get_all_orders(self):
        pass

    @abstractmethod
    def get_order_by_id(self, order_id):
        pass

    @abstractmethod
    def place_order(self, order):
        pass

    @abstractmethod
    def update_order_status(self, order_id, new_status):
        pass

    @abstractmethod
    def cancel_order(self, order_id):
        pass

    # Inventory operations
    @abstractmethod
    def get_inventory(self):
        pass

    @abstractmethod
    def get_product_inventory(self, product_id):
        pass

    @abstractmethod
    def update_inventory(self, inventory):
        pass

    @abstractmethod
    def get_low_stock_products(self, threshold):
        pass

    @abstractmethod
    def get_out_of_stock_products(self):
        pass

    # Reporting operations
    @abstractmethod
    def get_sales_report(self, start_date, end_date):
        pass

    @abstractmethod
    def get_customer_order_history(self, customer_id):
        pass