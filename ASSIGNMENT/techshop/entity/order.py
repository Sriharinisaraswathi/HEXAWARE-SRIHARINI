from datetime import datetime
from exception.incomplete_order_exception import IncompleteOrderException

class Order:
    def __init__(self, order_id, customer, order_date=None, total_amount=0.0, status="Pending"):
        self._order_id = int(order_id)
        self._customer = customer
        self._order_date = order_date if order_date else datetime.now()
        self._total_amount = float(total_amount) if total_amount else 0.0
        self._status = str(status) if status else "Pending"
        self._order_details = []

    @property
    def order_id(self):
        return self._order_id

    @property
    def customer(self):
        return self._customer

    @property
    def order_date(self):
        return self._order_date

    @property
    def total_amount(self):
        return self._total_amount

    @property
    def status(self):
        return self._status

    @property
    def order_details(self):
        return self._order_details

    def calculate_total_amount(self):
        try:
            self._total_amount = sum(detail.calculate_subtotal() for detail in self._order_details)
        except Exception as e:
            print(f"Error calculating order total: {e}")
            self._total_amount = 0.0
        return self._total_amount

    def get_order_details(self):
        try:
            details = [
                f"Order #{self._order_id}",
                f"Customer: {self._customer.first_name} {self._customer.last_name}",
                f"Date: {self._order_date.strftime('%Y-%m-%d %H:%M')}",
                f"Status: {self._status}",
                f"Total Amount: ₹{self._total_amount:.2f}",
                "Items:"
            ]
            
            for detail in self._order_details:
                details.append(f"- {detail.get_order_detail_info()}")
            
            return "\n".join(details)
        except Exception as e:
            print(f"Error generating order details: {e}")
            return f"Order #{self._order_id} (Error displaying details)"

    def update_order_status(self, new_status):
        valid_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
        if str(new_status) not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {valid_statuses}")
        self._status = str(new_status)

    def cancel_order(self, inventory):
        if self._status == "Cancelled":
            return
        
        self._status = "Cancelled"
        for detail in self._order_details:
            try:
                inventory.add_to_inventory(detail.product.product_id, detail.quantity)
            except Exception as e:
                print(f"Error returning inventory for order {self._order_id}: {e}")

    def add_order_detail(self, order_detail):
        if not order_detail or not order_detail.product:
            raise IncompleteOrderException("Order detail requires a valid product")
        
        try:
            self._order_details.append(order_detail)
            self.calculate_total_amount()
        except Exception as e:
            print(f"Error adding order detail: {e}")
            raise DatabaseException("Failed to add order item")