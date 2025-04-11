CREATE DATABASE Ecom;
Use Ecom;

--CREATE TABLE Customers
CREATE TABLE customers (
 customer_id INT PRIMARY KEY,
 name VARCHAR(100),
 email VARCHAR(100) UNIQUE,
 password VARCHAR(100) UNIQUE
);

--CREATE TABLE products
CREATE TABLE products (
  product_id INT PRIMARY KEY,
  name VARCHAR(100),
  price DECIMAL(10, 2),
  description TEXT,
  stockQuantity INT
);

--CREATE TABLE cart 
CREATE TABLE cart (
   cart_id INT PRIMARY KEY,
   customer_id INT,
   product_id INT,
   quantity INT,
   FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
   FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- CREATE TABLE orders
CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  customer_id INT,
  order_date DATE,
  total_price DECIMAL(10, 2),
  shipping_address TEXT,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- CREATE TABLE order_items
CREATE TABLE order_items (
  order_item_id INT PRIMARY KEY,
  order_id INT,
  product_id INT,
  quantity INT,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

--INSERT VALUES INTO TABLE CUSTOMERS

insert into customers (customer_id, name, email, password) values
(1, 'John Doe', 'johndoe@example.com', 'pass123john'),
(2, 'Jane Smith', 'janesmith@example.com', 'pass123jane'),
(3, 'Robert Johnson', 'robert@example.com', 'pass123rob'),
(4, 'Sarah Brown', 'sarah@example.com', 'pass123sarah'),
(5, 'David Lee', 'david@example.com', 'pass123david'),
(6, 'Laura Hall', 'laura@example.com', 'pass123laura'),
(7, 'Michael Davis', 'michael@example.com', 'pass123mike'),
(8, 'Emma Wilson', 'emma@example.com', 'pass123emma'),
(9, 'William Taylor', 'william@example.com', 'pass123will'),
(10, 'Olivia Adams', 'olivia@example.com', 'pass123olivia');

--INSERT VALUES INTO PRODUCTS TABLE 

insert into products (product_id, name, price, description, stockQuantity) values
(1, 'Laptop', 800.00, 'High-performance laptop', 10),
(2, 'Smartphone', 600.00, 'Latest smartphone', 15),
(3, 'Tablet', 300.00, 'Portable tablet', 20),
(4, 'Headphones', 150.00, 'Noise-canceling', 30),
(5, 'TV', 900.00, '4K Smart TV', 5),
(6, 'Coffee Maker', 50.00, 'Automatic coffee maker', 25),
(7, 'Refrigerator', 700.00, 'Energy-efficient', 10),
(8, 'Microwave Oven', 80.00, 'Countertop microwave', 15),
(9, 'Blender', 70.00, 'High-speed blender', 20),
(10, 'Vacuum Cleaner', 120.00, 'Bagless vacuum cleaner', 10);

--INSERT VALUES INTO ORDERS TABLE

insert into orders (order_id, customer_id, order_date, total_price, shipping_address) values
(1, 1, '2023-01-05', 1200.00, '123 Main St, City'),
(2, 2, '2023-02-10', 900.00, '456 Elm St, Town'),
(3, 3, '2023-03-15', 300.00, '789 Oak St, Village'),
(4, 4, '2023-04-20', 150.00, '101 Pine St, Suburb'),
(5, 5, '2023-05-25', 1800.00, '234 Cedar St, District'),
(6, 6, '2023-06-30', 400.00, '567 Birch St, County'),
(7, 7, '2023-07-05', 700.00, '890 Maple St, State'),
(8, 8, '2023-08-10', 160.00, '321 Redwood St, Country'),
(9, 9, '2023-09-15', 140.00, '432 Spruce St, Province'),
(10, 10, '2023-10-20', 1400.00, '765 Fir St, Territory');

--INSERT INTO ORDER_ITEMS TABLE 

insert into order_items (order_item_id, order_id, product_id, quantity) values
(1, 1, 1, 2),
(2, 1, 3, 1),
(3, 2, 2, 3),
(4, 3, 5, 2),
(5, 4, 4, 4),
(6, 4, 6, 1),
(7, 5, 1, 1),
(8, 5, 2, 2),
(9, 6, 10, 2),
(10, 6, 9, 3);

--INSERT VALUES INTO CART TABLE 

insert into cart (cart_id, customer_id, product_id, quantity) values
(1, 1, 1, 2),
(2, 1, 3, 1),
(3, 2, 2, 3),
(4, 3, 4, 4),
(5, 3, 5, 2),
(6, 4, 6, 1),
(7, 5, 1, 1),
(8, 6, 10, 2),
(9, 6, 9, 3),
(10, 7, 7, 2);

SELECT * FROM customers
SELECT * FROM products
SELECT * FROM cart
SELECT * FROM orders
SELECT * FROM order_items

--1.Update refrigerator product price to 800.

UPDATE products 
SET PRICE = 800 
WHERE name='Refrigerator';
SELECT * FROM products

--2.Remove all cart items for a specific customer.

DELETE FROM cart WHERE customer_id=2
SELECT * FROM cart

--3.Retrieve Products Priced Below $100.

SELECT product_id,name,price 
FROM products 
WHERE price < 100;

--4.Find Products with Stock Quantity Greater Than 5.

SELECT product_id,name,stockQuantity 
FROM products 
WHERE stockQuantity>5;

--5.Retrieve Orders with Total Amount Between $500 and $1000.

SELECT order_id,total_price 
FROM orders 
WHERE total_price BETWEEN 500 AND 1000;

--6.Find Products which name end with letter ‘r’.

SELECT product_id,name 
FROM  products  
WHERE name LIKE '%r';

--7.Retrieve Cart Items for Customer 5.

SELECT ca.cart_id, c.customer_id, c.name, p.name 
FROM customers c 
left join cart ca on c.customer_id=ca.customer_id 
join products p on p.product_id=ca.product_id 
WHERE c.customer_id=5;

--8.Find Customers Who Placed Orders in 2023.

SELECT C.customer_id,C.name,O.order_date 
FROM customers C 
join orders O on O.customer_id=C.customer_id 
WHERE YEAR(O.order_date)='2023';

--9.Determine the Minimum Stock Quantity for Each Product Category.
SELECT 
      CASE
	     WHEN name in ('Laptop', 'Smartphone', 'Tablet', 'TV') THEN 'ELECTRONICS'
		 WHEN name in ('Refrigerator', 'Microwave Oven','blender','coffee Maker','vaccum cleaner') THEN 'APPLIANCES'
		 WHEN name ='Headphones' THEN 'ACCESSORIES'
		 ELSE 'OTHERS'
	  END as Category,
MIN(stockQuantity) as mininum_stock
FROM products
group by
       CASE
	     WHEN name in ('Laptop', 'Smartphone', 'Tablet', 'TV') THEN 'ELECTRONICS'
		 WHEN name in ('Refrigerator', 'Microwave Oven','blender','coffee Maker','vaccum cleaner') THEN 'APPLIANCES'
		 WHEN name ='Headphones' THEN 'ACCESSORIES'
		 ELSE 'OTHERS'
	  END;

--10.Calculate the Total Amount Spent by Each Customer.

SELECT C.customer_id,C.name,SUM(O.total_price) as TOTAL_AMOUNT 
FROM customers C 
JOIN orders O on c.customer_id=o.customer_id 
group by C.name,C.customer_id
order by SUM(O.total_price) DESC;

--11.Find the Average Order Amount for Each Customer.

SELECT C.customer_id,C.name,AVG(O.total_price) as AVG_AMOUNT 
FROM customers C 
JOIN orders O on c.customer_id=o.customer_id 
group by C.name,C.customer_id
order by AVG(O.total_price) DESC;

--12.Count the Number of Orders Placed by Each Customer.

SELECT C.customer_id,C.name,COUNT(O.order_id) as number_of_order 
FROM customers C 
join Orders O on C.customer_id=O.customer_id 
group by c.name,c.customer_id 
order by c.customer_id asc;

--13.Find the Maximum Order Amount for Each Customer

SELECT C.Customer_id,C.name,MAX(O.total_price) as Maximum_amount 
from customers C 
JOIN orders O ON C.customer_id=O.customer_id 
GROUP BY c.customer_id,c.name 
order by MAX(o.total_price) desc;

--14.Get Customers Who Placed Orders Totaling Over $1000.

SELECT C.customer_id,C.name,SUM(O.total_price) as amount_spent 
FROM customers C 
JOIN orders O ON C.customer_id=O.customer_id 
GROUP BY C.name,C.customer_id 
HAVING SUM(O.total_price)>1000 
ORDER BY SUM(O.total_price) desc;

--15.Subquery to Find Products Not in the Cart.

SELECT p.product_id,p.name 
from products p 
where p.product_id not in (select  product_id from cart)

--16.Subquery to Find Customers Who Haven't Placed Orders.

SELECT C.customer_id,C.name 
FROM customers C 
WHERE C.customer_id NOT IN (SELECT  customer_id FROM orders);

--17.Subquery to Calculate the Percentage of Total Revenue for a Product.

SELECT  p.product_id, p.name,
ROUND(
  (SUM(o.quantity * p.price) * 100.0) /
  (SELECT SUM(o2.quantity * p2.price)
   from order_items o2
  JOIN products p2 ON o2.product_id = p2.product_id),2
    ) as revenue_percent
from order_items o
join products p ON o.product_id = p.product_id
group by p.product_id, p.name;

--18.Subquery to Find Products with Low Stock.

SELECT product_id , name , stockquantity 
from products where stockQuantity < (select avg(stockQuantity) from products)

--19.Subquery to Find Customers Who Placed High-Value Orders.

SELECT C.customer_id,C.name,o.total_price 
from customers C 
join orders o on c.customer_id=o.customer_id
where o.total_price > (select avg(o.total_price) from orders o) 
order by o.total_price desc;






































