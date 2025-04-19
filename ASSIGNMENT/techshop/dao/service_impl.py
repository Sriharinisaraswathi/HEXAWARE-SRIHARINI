import pyodbc
from datetime import datetime
from util.db_conn_util import get_connection
from exception.database_exception import DatabaseException
from exception.invalid_data_exception import InvalidDataException
from exception.insufficient_stock_exception import InsufficientStockException
from exception.incomplete_order_exception import IncompleteOrderException
from entity.customer import Customer
from entity.product import Product
from entity.order import Order
from entity.order_detail import OrderDetail
from entity.inventory import Inventory

class TechShopServiceImpl:
    def __init__(self, conn_string):
        self.conn = get_connection(conn_string)

    # ========== CUSTOMER OPERATIONS ==========
    def get_all_customers(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT CustomerID, FirstName, LastName, Email, Phone, Address 
                FROM Customers
                ORDER BY LastName, FirstName
            """)
            
            customers = []
            for row in cursor.fetchall():
                try:
                    customer = Customer(
                        customer_id=int(row[0]),
                        first_name=str(row[1]),
                        last_name=str(row[2]),
                        email=str(row[3]),
                        phone=str(row[4]),
                        address=str(row[5])
                    )
                    customers.append(customer)
                except Exception as e:
                    print(f"Error creating customer from row {row}: {e}")
                    continue
            
            return customers
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve customers: {str(e)}")

    def get_customer_by_id(self, customer_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT CustomerID, FirstName, LastName, Email, Phone, Address
                FROM Customers
                WHERE CustomerID = ?
            """, int(customer_id))
            
            row = cursor.fetchone()
            if not row:
                return None
                
            return Customer(
                customer_id=int(row[0]),
                first_name=str(row[1]),
                last_name=str(row[2]),
                email=str(row[3]),
                phone=str(row[4]),
                address=str(row[5])
            )
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve customer {customer_id}: {str(e)}")

    def add_customer(self, customer):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Customers (CustomerID, FirstName, LastName, Email, Phone, Address)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                int(customer.customer_id),
                str(customer.first_name),
                str(customer.last_name),
                str(customer.email),
                str(customer.phone),
                str(customer.address)
            ))
            self.conn.commit()
            return True
        except pyodbc.IntegrityError as e:
            if "Email" in str(e):
                raise InvalidDataException("Email address already exists")
            raise DatabaseException(f"Database integrity error: {str(e)}")
        except Exception as e:
            raise DatabaseException(f"Failed to add customer: {str(e)}")

    def update_customer(self, customer):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE Customers
                SET FirstName = ?, LastName = ?, Email = ?, Phone = ?, Address = ?
                WHERE CustomerID = ?
            """, (
                str(customer.first_name),
                str(customer.last_name),
                str(customer.email),
                str(customer.phone),
                str(customer.address),
                int(customer.customer_id)
            ))
            self.conn.commit()
            return cursor.rowcount > 0
        except pyodbc.IntegrityError as e:
            if "Email" in str(e):
                raise InvalidDataException("Email address already exists")
            raise DatabaseException(f"Database integrity error: {str(e)}")
        except Exception as e:
            raise DatabaseException(f"Failed to update customer: {str(e)}")

    def delete_customer(self, customer_id):
        try:
            cursor = self.conn.cursor()
            
            # Check for existing orders
            cursor.execute("""
                SELECT COUNT(*) FROM Orders WHERE CustomerID = ?
            """, int(customer_id))
            if cursor.fetchone()[0] > 0:
                raise DatabaseException("Cannot delete customer with existing orders")
                
            cursor.execute("""
                DELETE FROM Customers WHERE CustomerID = ?
            """, int(customer_id))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseException(f"Failed to delete customer: {str(e)}")

    # ========== PRODUCT OPERATIONS ==========
    def get_all_products(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT ProductID, ProductName, Description, Price
                FROM Products
                ORDER BY ProductName
            """)
            
            products = []
            for row in cursor.fetchall():
                try:
                    product = Product(
                        product_id=int(row[0]),
                        product_name=str(row[1]),
                        description=str(row[2]) if row[2] else "",
                        price=float(row[3]) if row[3] else 0.0
                    )
                    products.append(product)
                except Exception as e:
                    print(f"Error creating product from row {row}: {e}")
                    continue
            
            return products
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve products: {str(e)}")

    def get_product_by_id(self, product_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT ProductID, ProductName, Description, Price
                FROM Products
                WHERE ProductID = ?
            """, int(product_id))
            
            row = cursor.fetchone()
            if not row:
                return None
                
            return Product(
                product_id=int(row[0]),
                product_name=str(row[1]),
                description=str(row[2]) if row[2] else "",
                price=float(row[3]) if row[3] else 0.0
            )
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve product {product_id}: {str(e)}")

    def add_product(self, product):
        try:
            cursor = self.conn.cursor()
            cursor.execute("BEGIN TRANSACTION")
            
            try:
                # Insert product
                cursor.execute("""
                    INSERT INTO Products (ProductID, ProductName, Description, Price)
                    VALUES (?, ?, ?, ?)
                """, (
                    int(product.product_id),
                    str(product.product_name),
                    str(product.description) if product.description else "",
                    float(product.price) if product.price else 0.0
                ))
                
                # Add to inventory
                cursor.execute("""
                    DECLARE @next_id INT
                    SELECT @next_id = ISNULL(MAX(InventoryID), 0) + 1 FROM Inventory
                    
                    INSERT INTO Inventory (InventoryID, ProductID, QuantityInStock, LastStockUpdate)
                    VALUES (@next_id, ?, 0, GETDATE())
                """, int(product.product_id))
                
                cursor.execute("COMMIT TRANSACTION")
                self.conn.commit()
                return True
            except Exception as e:
                cursor.execute("ROLLBACK TRANSACTION")
                raise
        except pyodbc.IntegrityError as e:
            if "ProductName" in str(e):
                raise InvalidDataException("Product name already exists")
            raise DatabaseException(f"Database integrity error: {str(e)}")
        except Exception as e:
            raise DatabaseException(f"Failed to add product: {str(e)}")

    def update_product(self, product):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE Products
                SET ProductName = ?, Description = ?, Price = ?
                WHERE ProductID = ?
            """, (
                str(product.product_name),
                str(product.description) if product.description else "",
                float(product.price) if product.price else 0.0,
                int(product.product_id)
            ))
            self.conn.commit()
            return cursor.rowcount > 0
        except pyodbc.IntegrityError as e:
            if "ProductName" in str(e):
                raise InvalidDataException("Product name already exists")
            raise DatabaseException(f"Database integrity error: {str(e)}")
        except Exception as e:
            raise DatabaseException(f"Failed to update product: {str(e)}")

    def delete_product(self, product_id):
        try:
            cursor = self.conn.cursor()
            
            # Check for existing order details
            cursor.execute("""
                SELECT COUNT(*) FROM OrderDetails WHERE ProductID = ?
            """, int(product_id))
            if cursor.fetchone()[0] > 0:
                raise DatabaseException("Cannot delete product referenced in orders")
                
            cursor.execute("""
                DELETE FROM Inventory WHERE ProductID = ?
            """, int(product_id))
            
            cursor.execute("""
                DELETE FROM Products WHERE ProductID = ?
            """, int(product_id))
            
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseException(f"Failed to delete product: {str(e)}")

    # ========== ORDER OPERATIONS ==========
    def get_all_orders(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT o.OrderID, o.CustomerID, o.OrderDate, o.TotalAmount, o.Status,
                       c.FirstName, c.LastName, c.Email, c.Phone, c.Address
                FROM Orders o
                JOIN Customers c ON o.CustomerID = c.CustomerID
                ORDER BY o.OrderDate DESC
            """)
            
            orders = []
            for row in cursor.fetchall():
                try:
                    customer = Customer(
                        customer_id=int(row[1]),
                        first_name=str(row[5]),
                        last_name=str(row[6]),
                        email=str(row[7]),
                        phone=str(row[8]),
                        address=str(row[9])
                    )
                    
                    order = Order(
                        order_id=int(row[0]),
                        customer=customer,
                        order_date=row[2],
                        total_amount=float(row[3]) if row[3] else 0.0,
                        status=str(row[4]) if row[4] else "Pending"
                    )
                    
                    # Get order details
                    cursor.execute("""
                        SELECT od.OrderDetailID, od.OrderID, od.ProductID, od.Quantity,
                               p.ProductID, p.ProductName, p.Description, p.Price
                        FROM OrderDetails od
                        JOIN Products p ON od.ProductID = p.ProductID
                        WHERE od.OrderID = ?
                    """, int(row[0]))
                    
                    for detail_row in cursor.fetchall():
                        try:
                            product = Product(
                                product_id=int(detail_row[4]),
                                product_name=str(detail_row[5]),
                                description=str(detail_row[6]) if detail_row[6] else "",
                                price=float(detail_row[7]) if detail_row[7] else 0.0
                            )
                            
                            order_detail = OrderDetail(
                                order_detail_id=int(detail_row[0]),
                                order=order,
                                product=product,
                                quantity=int(detail_row[3])
                            )
                            order.add_order_detail(order_detail)
                        except Exception as e:
                            print(f"Error processing order detail {detail_row[0]}: {e}")
                            continue
                    
                    orders.append(order)
                except Exception as e:
                    print(f"Error processing order {row[0]}: {e}")
                    continue
            
            return orders
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve orders: {str(e)}")

    def get_order_by_id(self, order_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT o.OrderID, o.CustomerID, o.OrderDate, o.TotalAmount, o.Status,
                       c.FirstName, c.LastName, c.Email, c.Phone, c.Address
                FROM Orders o
                JOIN Customers c ON o.CustomerID = c.CustomerID
                WHERE o.OrderID = ?
            """, int(order_id))
            
            row = cursor.fetchone()
            if not row:
                return None
                
            customer = Customer(
                customer_id=int(row[1]),
                first_name=str(row[5]),
                last_name=str(row[6]),
                email=str(row[7]),
                phone=str(row[8]),
                address=str(row[9])
            )
            
            order = Order(
                order_id=int(row[0]),
                customer=customer,
                order_date=row[2],
                total_amount=float(row[3]) if row[3] else 0.0,
                status=str(row[4]) if row[4] else "Pending"
            )
            
            # Get order details
            cursor.execute("""
                SELECT od.OrderDetailID, od.OrderID, od.ProductID, od.Quantity,
                       p.ProductID, p.ProductName, p.Description, p.Price
                FROM OrderDetails od
                JOIN Products p ON od.ProductID = p.ProductID
                WHERE od.OrderID = ?
            """, int(order_id))
            
            for detail_row in cursor.fetchall():
                try:
                    product = Product(
                        product_id=int(detail_row[4]),
                        product_name=str(detail_row[5]),
                        description=str(detail_row[6]) if detail_row[6] else "",
                        price=float(detail_row[7]) if detail_row[7] else 0.0
                    )
                    
                    order_detail = OrderDetail(
                        order_detail_id=int(detail_row[0]),
                        order=order,
                        product=product,
                        quantity=int(detail_row[3])
                    )
                    order.add_order_detail(order_detail)
                except Exception as e:
                    print(f"Error processing order detail {detail_row[0]}: {e}")
                    continue
            
            return order
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve order {order_id}: {str(e)}")

    def place_order(self, order):
        try:
            cursor = self.conn.cursor()
            cursor.execute("BEGIN TRANSACTION")
            
            try:
                # Insert order header
                cursor.execute("""
                    INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount, Status)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    int(order.order_id),
                    int(order.customer.customer_id),
                    order.order_date,
                    float(order.total_amount),
                    str(order.status)
                ))
                
                # Process each order detail
                for detail in order.order_details:
                    # Verify stock availability
                    cursor.execute("""
                        SELECT QuantityInStock FROM Inventory WHERE ProductID = ?
                    """, int(detail.product.product_id))
                    stock = cursor.fetchone()
                    
                    if not stock or stock[0] < detail.quantity:
                        raise InsufficientStockException(
                            f"Insufficient stock for product {detail.product.product_id}"
                        )
                    
                    # Insert order detail
                    cursor.execute("""
                        INSERT INTO OrderDetails (OrderDetailID, OrderID, ProductID, Quantity)
                        VALUES (?, ?, ?, ?)
                    """, (
                        int(detail.order_detail_id),
                        int(order.order_id),
                        int(detail.product.product_id),
                        int(detail.quantity)
                    ))
                    
                    # Update inventory
                    cursor.execute("""
                        UPDATE Inventory
                        SET QuantityInStock = QuantityInStock - ?,
                            LastStockUpdate = GETDATE()
                        WHERE ProductID = ?
                    """, (
                        int(detail.quantity),
                        int(detail.product.product_id)
                    ))
                
                cursor.execute("COMMIT TRANSACTION")
                self.conn.commit()
                return True
            except Exception as e:
                cursor.execute("ROLLBACK TRANSACTION")
                raise
        except Exception as e:
            raise DatabaseException(f"Failed to place order: {str(e)}")

    def update_order_status(self, order_id, new_status):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE Orders
                SET Status = ?
                WHERE OrderID = ?
            """, (
                str(new_status),
                int(order_id)
            ))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseException(f"Failed to update order status: {str(e)}")

    def cancel_order(self, order_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("BEGIN TRANSACTION")
            
            try:
                # Get order details for inventory restoration
                cursor.execute("""
                    SELECT ProductID, Quantity
                    FROM OrderDetails
                    WHERE OrderID = ?
                """, int(order_id))
                
                details = cursor.fetchall()
                for product_id, quantity in details:
                    cursor.execute("""
                        UPDATE Inventory
                        SET QuantityInStock = QuantityInStock + ?,
                            LastStockUpdate = GETDATE()
                        WHERE ProductID = ?
                    """, (
                        int(quantity),
                        int(product_id)
                    ))
                
                # Update order status
                cursor.execute("""
                    UPDATE Orders
                    SET Status = 'Cancelled'
                    WHERE OrderID = ?
                """, int(order_id))
                
                cursor.execute("COMMIT TRANSACTION")
                self.conn.commit()
                return True
            except Exception as e:
                cursor.execute("ROLLBACK TRANSACTION")
                raise
        except Exception as e:
            raise DatabaseException(f"Failed to cancel order: {str(e)}")

    # ========== INVENTORY OPERATIONS ==========
    def get_inventory(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT i.InventoryID, i.ProductID, i.QuantityInStock, i.LastStockUpdate,
                       p.ProductName, p.Description, p.Price
                FROM Inventory i
                JOIN Products p ON i.ProductID = p.ProductID
                ORDER BY p.ProductName
            """)
            
            inventory_items = []
            for row in cursor.fetchall():
                try:
                    product = Product(
                        product_id=int(row[1]),
                        product_name=str(row[4]),
                        description=str(row[5]) if row[5] else "",
                        price=float(row[6]) if row[6] else 0.0
                    )
                    
                    inventory = Inventory(
                        inventory_id=int(row[0]),
                        product=product,
                        quantity_in_stock=int(row[2]),
                        last_stock_update=row[3]
                    )
                    inventory_items.append(inventory)
                except Exception as e:
                    print(f"Error creating inventory item from row {row}: {e}")
                    continue
            
            return inventory_items
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve inventory: {str(e)}")

    def get_product_inventory(self, product_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT i.InventoryID, i.ProductID, i.QuantityInStock, i.LastStockUpdate,
                       p.ProductName, p.Description, p.Price
                FROM Inventory i
                JOIN Products p ON i.ProductID = p.ProductID
                WHERE i.ProductID = ?
            """, int(product_id))
            
            row = cursor.fetchone()
            if not row:
                return None
                
            product = Product(
                product_id=int(row[1]),
                product_name=str(row[4]),
                description=str(row[5]) if row[5] else "",
                price=float(row[6]) if row[6] else 0.0
            )
            
            return Inventory(
                inventory_id=int(row[0]),
                product=product,
                quantity_in_stock=int(row[2]),
                last_stock_update=row[3]
            )
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve inventory for product {product_id}: {str(e)}")

    def update_inventory(self, inventory):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE Inventory
                SET QuantityInStock = ?, LastStockUpdate = GETDATE()
                WHERE ProductID = ?
            """, (
                int(inventory.quantity_in_stock),
                int(inventory.product.product_id)
            ))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseException(f"Failed to update inventory: {str(e)}")

    def get_low_stock_products(self, threshold):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT i.InventoryID, i.ProductID, i.QuantityInStock, i.LastStockUpdate,
                       p.ProductName, p.Description, p.Price
                FROM Inventory i
                JOIN Products p ON i.ProductID = p.ProductID
                WHERE i.QuantityInStock < ?
                ORDER BY i.QuantityInStock
            """, int(threshold))
            
            low_stock_items = []
            for row in cursor.fetchall():
                try:
                    product = Product(
                        product_id=int(row[1]),
                        product_name=str(row[4]),
                        description=str(row[5]) if row[5] else "",
                        price=float(row[6]) if row[6] else 0.0
                    )
                    
                    inventory = Inventory(
                        inventory_id=int(row[0]),
                        product=product,
                        quantity_in_stock=int(row[2]),
                        last_stock_update=row[3]
                    )
                    low_stock_items.append(inventory)
                except Exception as e:
                    print(f"Error creating low stock item from row {row}: {e}")
                    continue
            
            return low_stock_items
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve low stock products: {str(e)}")

    def get_out_of_stock_products(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT i.InventoryID, i.ProductID, i.QuantityInStock, i.LastStockUpdate,
                       p.ProductName, p.Description, p.Price
                FROM Inventory i
                JOIN Products p ON i.ProductID = p.ProductID
                WHERE i.QuantityInStock = 0
                ORDER BY p.ProductName
            """)
            
            out_of_stock_items = []
            for row in cursor.fetchall():
                try:
                    product = Product(
                        product_id=int(row[1]),
                        product_name=str(row[4]),
                        description=str(row[5]) if row[5] else "",
                        price=float(row[6]) if row[6] else 0.0
                    )
                    
                    inventory = Inventory(
                        inventory_id=int(row[0]),
                        product=product,
                        quantity_in_stock=int(row[2]),
                        last_stock_update=row[3]
                    )
                    out_of_stock_items.append(inventory)
                except Exception as e:
                    print(f"Error creating out of stock item from row {row}: {e}")
                    continue
            
            return out_of_stock_items
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve out of stock products: {str(e)}")

    # ========== REPORTING OPERATIONS ==========
    def get_sales_report(self, start_date, end_date):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT 
                    p.ProductID, p.ProductName, 
                    SUM(od.Quantity) as TotalSold, 
                    SUM(od.Quantity * p.Price) as TotalRevenue
                FROM OrderDetails od
                JOIN Products p ON od.ProductID = p.ProductID
                JOIN Orders o ON od.OrderID = o.OrderID
                WHERE o.OrderDate BETWEEN ? AND ?
                  AND o.Status != 'Cancelled'
                GROUP BY p.ProductID, p.ProductName
                ORDER BY TotalRevenue DESC
            """, (start_date, end_date))
            
            report = []
            for row in cursor.fetchall():
                report.append({
                    'product_id': int(row[0]),
                    'product_name': str(row[1]),
                    'total_sold': int(row[2]),
                    'total_revenue': float(row[3]) if row[3] else 0.0
                })
            
            return report
        except Exception as e:
            raise DatabaseException(f"Failed to generate sales report: {str(e)}")

    def get_customer_order_history(self, customer_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT 
                    o.OrderID, o.OrderDate, o.TotalAmount, o.Status,
                    COUNT(od.OrderDetailID) as ItemCount
                FROM Orders o
                LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
                WHERE o.CustomerID = ?
                GROUP BY o.OrderID, o.OrderDate, o.TotalAmount, o.Status
                ORDER BY o.OrderDate DESC
            """, int(customer_id))
            
            history = []
            for row in cursor.fetchall():
                history.append({
                    'order_id': int(row[0]),
                    'order_date': row[1],
                    'total_amount': float(row[2]) if row[2] else 0.0,
                    'status': str(row[3]) if row[3] else "Unknown",
                    'item_count': int(row[4])
                })
            
            return history
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve customer order history: {str(e)}")

    # ========== HELPER METHODS ==========
    def get_next_customer_id(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ISNULL(MAX(CustomerID), 0) + 1 FROM Customers")
            return int(cursor.fetchone()[0])
        except Exception as e:
            raise DatabaseException(f"Failed to get next customer ID: {str(e)}")

    def get_next_product_id(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ISNULL(MAX(ProductID), 0) + 1 FROM Products")
            return int(cursor.fetchone()[0])
        except Exception as e:
            raise DatabaseException(f"Failed to get next product ID: {str(e)}")

    def get_next_order_id(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ISNULL(MAX(OrderID), 0) + 1 FROM Orders")
            return int(cursor.fetchone()[0])
        except Exception as e:
            raise DatabaseException(f"Failed to get next order ID: {str(e)}")

    def get_next_order_detail_id(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ISNULL(MAX(OrderDetailID), 0) + 1 FROM OrderDetails")
            return int(cursor.fetchone()[0])
        except Exception as e:
            raise DatabaseException(f"Failed to get next order detail ID: {str(e)}")

    def get_next_inventory_id(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT ISNULL(MAX(InventoryID), 0) + 1 FROM Inventory")
            return int(cursor.fetchone()[0])
        except Exception as e:
            raise DatabaseException(f"Failed to get next inventory ID: {str(e)}")

    def close(self):
        try:
            if self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Error closing connection: {e}")