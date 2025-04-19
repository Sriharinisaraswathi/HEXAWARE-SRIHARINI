from datetime import datetime
from dao.service_impl import TechShopServiceImpl
from util.db_property_util import get_connection_string
from exception.database_exception import DatabaseException
from exception.invalid_data_exception import InvalidDataException
from exception.insufficient_stock_exception import InsufficientStockException
from exception.incomplete_order_exception import IncompleteOrderException

def display_menu():
    print("\n=== TechShop Management System ===")
    print("1. Customer Management")
    print("2. Product Management")
    print("3. Order Management")
    print("4. Inventory Management")
    print("5. Reports")
    print("6. Exit")
    return input("Enter your choice (1-6): ")

def customer_management(service):
    while True:
        print("\n--- Customer Management ---")
        print("1. List all customers")
        print("2. Add new customer")
        print("3. Update customer")
        print("4. Delete customer")
        print("5. View customer details")
        print("6. Back to main menu")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            try:
                customers = service.get_all_customers()
                for cust in customers:
                    print(cust.get_customer_details())
                    print("--------------------")
            except DatabaseException as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            try:
                cust_id = service.get_next_customer_id()
                print(f"New Customer ID: {cust_id}")
                fname = input("First Name: ")
                lname = input("Last Name: ")
                email = input("Email: ")
                phone = input("Phone: ")
                address = input("Address: ")
                
                customer = Customer(cust_id, fname, lname, email, phone, address)
                service.add_customer(customer)
                print("Customer added successfully!")
            except InvalidDataException as e:
                print(f"Validation Error: {e}")
            except DatabaseException as e:
                print(f"Database Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "3":
            try:
                cust_id = int(input("Enter Customer ID to update: "))
                customer = service.get_customer_by_id(cust_id)
                if not customer:
                    print("Customer not found!")
                    continue
                    
                print("Current details:")
                print(customer.get_customer_details())
                
                print("\nEnter new details (leave blank to keep current):")
                fname = input(f"First Name [{customer.first_name}]: ") or customer.first_name
                lname = input(f"Last Name [{customer.last_name}]: ") or customer.last_name
                email = input(f"Email [{customer.email}]: ") or customer.email
                phone = input(f"Phone [{customer.phone}]: ") or customer.phone
                address = input(f"Address [{customer.address}]: ") or customer.address
                
                customer.first_name = fname
                customer.last_name = lname
                customer.email = email
                customer.phone = phone
                customer.address = address
                
                service.update_customer(customer)
                print("Customer updated successfully!")
            except InvalidDataException as e:
                print(f"Validation Error: {e}")
            except DatabaseException as e:
                print(f"Database Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "4":
            try:
                cust_id = int(input("Enter Customer ID to delete: "))
                service.delete_customer(cust_id)
                print("Customer deleted successfully!")
            except DatabaseException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "5":
            try:
                cust_id = int(input("Enter Customer ID: "))
                customer = service.get_customer_by_id(cust_id)
                if not customer:
                    print("Customer not found!")
                    continue
                    
                print("\nCustomer Details:")
                print(customer.get_customer_details())
                
                print("\nOrder History:")
                history = service.get_customer_order_history(cust_id)
                if not history:
                    print("No orders found")
                else:
                    for order in history:
                        print(f"Order #{order['order_id']} - {order['order_date']} - {order['status']}")
                        print(f"Items: {order['item_count']} - Total: ₹{order['total_amount']:.2f}")
                        print("--------------------")
            except DatabaseException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "6":
            break
            
        else:
            print("Invalid choice!")

def product_management(service):
    while True:
        print("\n--- Product Management ---")
        print("1. List all products")
        print("2. Add new product")
        print("3. Update product")
        print("4. Delete product")
        print("5. View product details")
        print("6. Back to main menu")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            try:
                products = service.get_all_products()
                for prod in products:
                    print(prod.get_product_details())
                    print("--------------------")
            except DatabaseException as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            try:
                prod_id = service.get_next_product_id()
                print(f"New Product ID: {prod_id}")
                name = input("Product Name: ")
                desc = input("Description: ")
                price = float(input("Price: "))
                
                product = Product(prod_id, name, desc, price)
                service.add_product(product)
                print("Product added successfully!")
            except InvalidDataException as e:
                print(f"Validation Error: {e}")
            except DatabaseException as e:
                print(f"Database Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "3":
            try:
                prod_id = int(input("Enter Product ID to update: "))
                product = service.get_product_by_id(prod_id)
                if not product:
                    print("Product not found!")
                    continue
                    
                print("Current details:")
                print(product.get_product_details())
                
                print("\nEnter new details (leave blank to keep current):")
                name = input(f"Name [{product.product_name}]: ") or product.product_name
                desc = input(f"Description [{product.description}]: ") or product.description
                price = input(f"Price [{product.price}]: ")
                price = float(price) if price else product.price
                
                product.product_name = name
                product.description = desc
                product.price = price
                
                service.update_product(product)
                print("Product updated successfully!")
            except InvalidDataException as e:
                print(f"Validation Error: {e}")
            except DatabaseException as e:
                print(f"Database Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "4":
            try:
                prod_id = int(input("Enter Product ID to delete: "))
                service.delete_product(prod_id)
                print("Product deleted successfully!")
            except DatabaseException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "5":
            try:
                prod_id = int(input("Enter Product ID: "))
                product = service.get_product_by_id(prod_id)
                if not product:
                    print("Product not found!")
                    continue
                    
                print("\nProduct Details:")
                print(product.get_product_details())
                
                # Show inventory status
                inventory = service.get_product_inventory(prod_id)
                if inventory:
                    print(f"\nInventory Status: {inventory.get_quantity_in_stock()} in stock")
                    if inventory.is_low_stock(5):
                        print("Warning: Low stock!")
                    if inventory.is_out_of_stock():
                        print("Warning: Out of stock!")
                else:
                    print("\nInventory information not available")
            except DatabaseException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "6":
            break
            
        else:
            print("Invalid choice!")

def order_management(service):
    while True:
        print("\n--- Order Management ---")
        print("1. List all orders")
        print("2. Place new order")
        print("3. Update order status")
        print("4. Cancel order")
        print("5. View order details")
        print("6. Back to main menu")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            try:
                orders = service.get_all_orders()
                for order in orders:
                    print(order.get_order_details())
                    print("--------------------")
            except DatabaseException as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            try:
                # Get customer ID
                cust_id = int(input("Enter Customer ID: "))
                customer = service.get_customer_by_id(cust_id)
                if not customer:
                    print("Customer not found!")
                    continue
                    
                # Create order
                order_id = service.get_next_order_id()
                order = Order(order_id, customer)
                
                # Add products to order
                while True:
                    print("\nCurrent Order:")
                    if order.order_details:
                        for detail in order.order_details:
                            print(detail.get_order_detail_info())
                        print(f"Total: ₹{order.calculate_total_amount():.2f}")
                    else:
                        print("No items in order yet")
                    
                    print("\n1. Add product to order")
                    print("2. Remove product from order")
                    print("3. Finalize order")
                    print("4. Cancel order creation")
                    
                    sub_choice = input("Enter choice: ")
                    
                    if sub_choice == "1":
                        prod_id = int(input("Enter Product ID: "))
                        product = service.get_product_by_id(prod_id)
                        if not product:
                            print("Product not found!")
                            continue
                            
                        inventory = service.get_product_inventory(prod_id)
                        if not inventory or inventory.is_out_of_stock():
                            print("Product is out of stock!")
                            continue
                            
                        print(f"Current stock: {inventory.get_quantity_in_stock()}")
                        quantity = int(input("Enter quantity: "))
                        
                        if quantity <= 0:
                            print("Quantity must be positive")
                            continue
                            
                        if not inventory.is_product_available(quantity):
                            print(f"Only {inventory.get_quantity_in_stock()} available!")
                            continue
                            
                        detail_id = service.get_next_order_detail_id()
                        order_detail = OrderDetail(detail_id, order, product, quantity)
                        order.add_order_detail(order_detail)
                        print("Product added to order!")
                        
                    elif sub_choice == "2":
                        if not order.order_details:
                            print("No items to remove")
                            continue
                            
                        for i, detail in enumerate(order.order_details, 1):
                            print(f"{i}. {detail.get_order_detail_info()}")
                            
                        item_num = int(input("Enter item number to remove: ")) - 1
                        if 0 <= item_num < len(order.order_details):
                            order.order_details.pop(item_num)
                            order.calculate_total_amount()
                            print("Item removed from order!")
                        else:
                            print("Invalid item number")
                            
                    elif sub_choice == "3":
                        if not order.order_details:
                            print("Cannot place empty order!")
                            continue
                            
                        service.place_order(order)
                        print(f"Order #{order_id} placed successfully!")
                        break
                        
                    elif sub_choice == "4":
                        print("Order creation cancelled")
                        break
                        
                    else:
                        print("Invalid choice!")
                        
            except InsufficientStockException as e:
                print(f"Inventory Error: {e}")
            except IncompleteOrderException as e:
                print(f"Order Error: {e}")
            except DatabaseException as e:
                print(f"Database Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "3":
            try:
                order_id = int(input("Enter Order ID: "))
                order = service.get_order_by_id(order_id)
                if not order:
                    print("Order not found!")
                    continue
                    
                print("Current status:", order.status)
                print("Available statuses: Pending, Processing, Shipped, Delivered, Cancelled")
                new_status = input("Enter new status: ")
                
                service.update_order_status(order_id, new_status)
                print("Order status updated successfully!")
            except DatabaseException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "4":
            try:
                order_id = int(input("Enter Order ID to cancel: "))
                service.cancel_order(order_id)
                print("Order cancelled successfully!")
            except DatabaseException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "5":
            try:
                order_id = int(input("Enter Order ID: "))
                order = service.get_order_by_id(order_id)
                if not order:
                    print("Order not found!")
                    continue
                    
                print("\nOrder Details:")
                print(order.get_order_details())
            except DatabaseException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "6":
            break
            
        else:
            print("Invalid choice!")

def inventory_management(service):
    while True:
        print("\n--- Inventory Management ---")
        print("1. View all inventory")
        print("2. View low stock items")
        print("3. View out of stock items")
        print("4. Update product stock")
        print("5. Back to main menu")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            try:
                inventory = service.get_inventory()
                for item in inventory:
                    product = item.product
                    print(f"{product.product_name} (ID: {product.product_id})")
                    print(f"Stock: {item.quantity_in_stock} - Last Updated: {item.last_stock_update}")
                    print(f"Value: ₹{item.get_inventory_value():.2f}")
                    print("--------------------")
            except DatabaseException as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            try:
                threshold = int(input("Enter low stock threshold: "))
                low_stock = service.get_low_stock_products(threshold)
                
                if not low_stock:
                    print(f"No products below {threshold} in stock")
                    continue
                    
                print(f"\nLow Stock Items (below {threshold}):")
                for item in low_stock:
                    product = item.product
                    print(f"{product.product_name} (ID: {product.product_id}): {item.quantity_in_stock} in stock")
            except DatabaseException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "3":
            try:
                out_of_stock = service.get_out_of_stock_products()
                
                if not out_of_stock:
                    print("No products are out of stock")
                    continue
                    
                print("\nOut of Stock Items:")
                for item in out_of_stock:
                    product = item.product
                    print(f"{product.product_name} (ID: {product.product_id})")
            except DatabaseException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "4":
            try:
                prod_id = int(input("Enter Product ID: "))
                inventory = service.get_product_inventory(prod_id)
                if not inventory:
                    print("Product not found in inventory!")
                    continue
                    
                print(f"Current stock: {inventory.quantity_in_stock}")
                new_quantity = int(input("Enter new quantity: "))
                
                if new_quantity < 0:
                    print("Quantity cannot be negative")
                    continue
                    
                inventory.update_stock_quantity(new_quantity)
                service.update_inventory(inventory)
                print("Inventory updated successfully!")
            except DatabaseException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "5":
            break
            
        else:
            print("Invalid choice!")

def reports(service):
    while True:
        print("\n--- Reports ---")
        print("1. Sales Report")
        print("2. Back to main menu")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            try:
                print("Enter date range for sales report (YYYY-MM-DD)")
                start_date = input("Start Date: ")
                end_date = input("End Date: ")
                
                report = service.get_sales_report(start_date, end_date)
                
                if not report:
                    print("No sales data for the selected period")
                    continue
                    
                total_revenue = sum(item['total_revenue'] for item in report)
                print(f"\nSales Report from {start_date} to {end_date}")
                print(f"Total Revenue: ₹{total_revenue:.2f}")
                print("\nProduct Sales:")
                for item in report:
                    print(f"{item['product_name']} (ID: {item['product_id']})")
                    print(f"Sold: {item['total_sold']} - Revenue: ₹{item['total_revenue']:.2f}")
                    print("--------------------")
            except DatabaseException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")
                
        elif choice == "2":
            break
            
        else:
            print("Invalid choice!")

def main():
    conn_str = get_connection_string("db.properties")
    service = TechShopServiceImpl(conn_str)
    
    try:
        while True:
            choice = display_menu()
            
            if choice == "1":
                customer_management(service)
            elif choice == "2":
                product_management(service)
            elif choice == "3":
                order_management(service)
            elif choice == "4":
                inventory_management(service)
            elif choice == "5":
                reports(service)
            elif choice == "6":
                print("Exiting TechShop Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    finally:
        service.close()

if __name__ == "__main__":
    from entity.customer import Customer
    from entity.product import Product
    from entity.order import Order
    from entity.order_detail import OrderDetail
    from entity.inventory import Inventory
    main()