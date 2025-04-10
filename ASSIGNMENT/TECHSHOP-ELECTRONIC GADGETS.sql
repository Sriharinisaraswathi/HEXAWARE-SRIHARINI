--Creating table customers
CREATE TABLE Customers(
  CustomerId int primary key,
  FirstName varchar(50),
  LastName varchar(50),
  Email varchar(100),
  Phone varchar(50),
  Address varchar(255));
--table products
CREATE TABLE Products(
  ProductId int primary key,
  ProductName varchar(50),
  Description Text,
  Price decimal(10,2));
--table orders
CREATE TABLE Orders(
  OrderId int primary key,
  CustomerId int,
  OrderDate date,
  TotalAmount decimal(10, 2),
  FOREIGN KEY (CustomerId)References Customers(CustomerId));
--table orderDetails
CREATE TABLE OrderDetails(
  OrderDetailId int primary key,
  OrderId int,
  ProductId int,
  Quantity int,
  FOREIGN KEY (OrderId) references Orders(OrderId),
  FOREIGN KEY (ProductId) references Products(ProductId));
--table inventory
CREATE TABLE Inventory (
  InventoryID int primary key,
  ProductID int,
  QuantityInStock int,
  LastStockUpdate datetime,
FOREIGN KEY (ProductID) REFERENCES Products(ProductID));

--inserting into customers 

INSERT INTO Customers values
(1, 'sri', 'harini', 'sri123@gmail.com', '1234567890', '123 Main St'),
(2, 'hema', 'malini', 'hema123@gmail.com', '2345678901', '456 Oak Ave'),
(3, 'prasana', 'ravi', 'ravi123@gmail.com', '3456789012', '789 Pine Rd'),
(4, 'robert', 'Brown', 'robert123@gmail.com', '4567890123', '321 Elm St'),
(5, 'Charlie', 'Davis', 'charles123@gmail.com', '5678901234', '654 Cedar Blvd'),
(6, 'shruthi', 'raj', 'raj123@gmail.com', '6789012345', '987 Maple Ln'),
(7, 'rahul', 'kumar', 'rahul123@gmail.com', '7890123456', '147 Spruce Way'),
(8, 'Grace', 'joseph', 'grace123@gmail.com', '8901234567', '258 Birch Dr'),
(9, 'rohith', 'sharma', 'rohith123@gmail.com', '9012345678', '369 Aspen Cir'),
(10, 'virat', 'kholi', 'virat123@gmail.com', '0123456789', '159 Walnut Ct');

--insert products

INSERT INTO Products values
(1, 'Smartphone', 'Latest model smartphone with 128GB storage', 699.99),
(2, 'Laptop', '14-inch lightweight laptop with 8GB RAM', 999.99),
(3, 'Headphones', 'Noise-cancelling over-ear headphones', 199.99),
(4, 'Smartwatch', 'Fitness tracking smartwatch', 149.99),
(5, 'Tablet', '10-inch display tablet with stylus', 349.99),
(6, 'Wireless Mouse', 'Ergonomic wireless mouse', 29.99),
(7, 'Keyboard', 'Mechanical keyboard with backlight', 59.99),
(8, 'Webcam', '1080p HD USB webcam', 79.99),
(9, 'Portable Charger', '10000mAh power bank', 39.99),
(10, 'Bluetooth Speaker', 'Compact wireless speaker', 89.99);
 
 --inserting orders values

insert into Orders values
(1, 1, '2024-03-01', 749.98),
(2, 2, '2024-03-03', 999.99),
(3, 3, '2024-03-05', 229.98),
(4, 4, '2024-03-07', 149.99),
(5, 5, '2024-03-09', 399.98),
(6, 6, '2024-03-11', 699.99),
(7, 7, '2024-03-13', 149.98),
(8, 8, '2024-03-15', 139.98),
(9, 9, '2024-03-17', 1099.98),
(10, 10, '2024-03-19', 199.99);

--inserting order values

INSERT INTO OrderDetails VALUES
(1, 1, 1, 1),   
(2, 1, 6, 1),  
(3, 2, 2, 1),  
(4, 3, 3, 1),  
(5, 3, 6, 1),   
(6, 4, 4, 1),   
(7, 5, 5, 1),   
(8, 5, 6, 1),   
(9, 6, 1, 1),   
(10, 7, 4, 1);

--insering inventory values

insert into Inventory values
(1, 1, 50, '2024-03-01 09:00:00'),
(2, 2, 30, '2024-03-01 09:15:00'),
(3, 3, 75, '2024-03-01 09:30:00'),
(4, 4, 60, '2024-03-01 09:45:00'),
(5, 5, 40, '2024-03-01 10:00:00'),
(6, 6, 100, '2024-03-01 10:15:00'),
(7, 7, 80, '2024-03-01 10:30:00'),
(8, 8, 45, '2024-03-01 10:45:00'),
(9, 9, 90, '2024-03-01 11:00:00'),
(10, 10, 70, '2024-03-01 11:15:00');

--selecting all the fields from every table

select * from customers
select * from Products
select * from Orders
select * from OrderDetails
select * from Inventory

--TASK2
--1 retrieve the names and emails of all customers

select FirstName,LastName,Email from Customers

--2 all orders with their order dates and corresponding customer 

select Orders.OrderId,Orders.OrderDate,Customers.FirstName,Customers.LastName 
from Orders,Customers 
where Orders.OrderId=Customers.CustomerId

--3 new customer record

insert into Customers (CustomerID, FirstName, LastName, Email, Phone, Address) values (11, 'Anjali', 'mohan', 'anjali123@gmail.com', '9876543210', '111 Rose Lane');
select * from Customers

--4 updating prices by 10%

update Products set price = price * 1.10 
where productName IN ('Smartphone','Laptop','Headphones','Tablet','wireless mouse','keyboard','Webcam','portable charger','Bluetooth Speaker')
select * from Products

--5 SQL query to delete a specific order and its associated order details from the "Orders" and "OrderDetails" tables

DELETE FROM OrderDetails WHERE OrderID = 1;
DELETE FROM Orders WHERE OrderID = 1;
select * from OrderDetails

--6 insert a new order into the "Orders" table.

insert into orders(OrderId,CustomerId,OrderDate,TotalAmount)values(11,11,'2024-04-01',1000.00);
select * from orders

--7 update the contact information

update Customers
set  Email='sriharini123@gmail.com',Phone=1234567231,Address='234 main street' 
where CustomerId=1
select * from Customers

--8 recalculate total cost 

UPDATE Orders set TotalAmount = ( SELECT SUM(od.Quantity * p.Price)
    from OrderDetails od
    JOIN Products p ON od.ProductID = p.ProductID
    where od.OrderID = Orders.OrderID
);
SELECT * FROM Orders

--9 new product

insert into Products(ProductId,ProductName,Description,Price)values(11,'monitor','3d display',2000.00);
select * from Products

--10 update status 

ALTER TABLE orders ADD status varchar(50);
select * from Orders
update Orders set status='Shipped' where OrderId between 5 and 11
select * from Orders

--11 calculate and update the number of orders placed by each customer in the "Customers" table based on the data in the "Orders" table.Add column if not exists

ALTER TABLE Customers ADD Order_Count INT DEFAULT 0;
select * from Customers

-- 12 Update order count

UPDATE Customers SET Order_Count = ( SELECT COUNT(*) FROM Orders WHERE Orders.CustomerID = Customers.CustomerID);
select * from Customers


--TASK3

--1 retrieve a list of all orders along with customer information

select O.OrderId,C.CustomerId,C.FirstName,C.LastName,C.Email,C.Address,C.Phone 
from orders O
join customers C on C.CustomerId=O.CustomerId;

--2 find the total revenue generated by each electronic gadget product.Include the product name and the total revenue

select p.productname,sum(od.Quantity*p.Price)as total_revenue 
from OrderDetails od 
join Products p on p.ProductId=od.ProductId
group by p.ProductName 
order by total_revenue desc

--3 list all customers who have made at least one purchase

select CONCAT(c.firstname,' ',c.lastname)as customername,count(o.orderid) as ordercount
from orders o
join Customers c on c.CustomerId=o.CustomerId  
group by c.CustomerId,c.FirstName,c.LastName 
having count(o.orderid)>=1

--4 most popular electronic gadget, which is the one with the highest total quantity ordered. Include the product name and the total quantity ordered.

select top 1 P.productName,SUM(OD.quantity)as highquantity 
from Products P 
join OrderDetails OD on P.ProductId=OD.ProductId 
group by P.ProductName 
ORDER BY highquantity desc;

--5 retrieve a list of electronic gadgets along with their corresponding categories.

SELECT ProductName,
    CASE
        WHEN ProductName IN ('Smartphone', 'Tablet', 'Laptop') THEN 'Mobile Devices'
        WHEN ProductName IN ('Headphones', 'Wireless Mouse','keyboard','webcam','portable charger','bluetooth speaker') THEN 'Accessories'
        WHEN ProductName = 'Smartwatch' THEN 'Wearables'
        ELSE 'Other'
    END AS Category
FROM Products;

--6 calculate the average order value for each customer. Include the customer's name and their average order value.

select c.firstname,c.lastname,avg(o.totalamount) as average_order 
from Customers c 
join Orders o on c.CustomerId=o.CustomerId
group by c.FirstName ,c.LastName;

--7 the order with the highest total revenue. Include the order ID, customer information, and the total revenue.

select top 1 O.orderid,c.firstname,c.lastname,O.totalamount as highest_revenue 
from Orders O join Customers C on O.CustomerId=c.CustomerId 
order by O.TotalAmount desc ;

--8 electronic gadgets and the number of times each product has been ordered.

SELECT p.ProductName,COUNT(od.OrderDetailID) AS TimesOrdered 
FROM OrderDetails od 
JOIN  Products p ON od.ProductID = p.ProductID 
GROUP BY p.ProductName
ORDER BY TimesOrdered DESC;

-- 9 find customers who have purchased a specific electronic gadget product.

SELECT DISTINCT c.FirstName, c.LastName, c.Email, c.Phone,p.ProductName
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
JOIN OrderDetails od ON o.OrderID = od.OrderID
JOIN Products p ON od.ProductID = p.ProductID
WHERE  p.ProductName = 'smartwatch';

--10 total revenue generated by all orders placed within a specific time period.
SELECT  SUM(TotalAmount) AS TotalRevenue 
FROM Orders
WHERE OrderDate BETWEEN '2024-03-17'AND '2024-03-07';
select * from Orders

--TASK 4 

--1find out which customers have not placed any orders.

select C.customerId,C.Firstname,C.Lastname  
from Customers C 
where C.CustomerId not in (select O.orderId from Orders O)

--2find the total number of products available for sale.

select (select count(*) from Products) as total_prod

--3calculate the total revenue generated by TechShop

select (SELECT sum(totalamount) FROM Orders) AS total_revenue;

--4calculate the average quantity ordered for products in a specific category

alter table products add  category varchar(50);
update Products set category=
case
	when ProductName in ('Smartphone', 'Tablet', 'Laptop') then 'mobile devices'
    when ProductName  in ('Headphones', 'Wireless Mouse','keyboard','webcam','portable charger','bluetooth speaker') THEN 'Accessories'
	when ProductName = 'Smartwatch' then 'Wearables'
	else 'others'
end
select * from Products
select ( select avg(o.quantity) 
from OrderDetails o 
where o.ProductId in (select p.productid from Products p where category='mobile devices')) as total_quantity

--5total revenue generated by a specific customer input customerid

select(select sum(o.totalamount) 
from Orders o 
where o.CustomerId in (select c.customerid from Customers c where CustomerId=3)) as total_revenue

--6customers who have placed the most orders. List their names and the number of orders they've placed.

SELECT TOP 1 c.CustomerId,c.FirstName,c.LastName,COUNT(o.OrderId) AS total_orders
FROM Customers c
JOIN Orders o ON c.CustomerId = o.CustomerId
GROUP BY c.CustomerId, c.FirstName, c.LastName
ORDER BY total_orders DESC;

--7find the most popular product category, which is the one with the highest total quantity ordered across all orders.
 ALTER TABLE products ADD categories VARCHAR(50);
  update products set Categories= 
  CASE
        WHEN ProductName IN ('Smartphone', 'Tablet', 'Laptop') THEN 'Mobile Devices'
        WHEN ProductName IN ('Headphones', 'Wireless Mouse','keyboard','webcam','portable charger','bluetooth speaker') THEN 'Accessories'
        WHEN ProductName = 'Smartwatch' THEN 'Wearables'
        ELSE 'Other'
    END
	select * from products
select top 1 p.categories,sum(o.quantity) as total_quantity from orderdetails o join products p on p.productid=o.productid group by p.categories 
order by total_quantity desc 

--8find the customer who has spent the most money (highest total revenue) on electronic gadgets with names and total spendings

select top 1 c.firstname,c.lastname,sum(o.totalamount) as total_revenue 
from Orders o
join Customers c on c.CustomerId=o.CustomerId 
group by c.FirstName,c.LastName 
order by total_revenue desc

--9calculate the average order value for all customers.

select AVG(totalamount) as average_order from Orders 

--10find the total number of orders placed by each customer and list their names along with the order count.

select c.CustomerId,c.firstname,c.lastname,COUNT(o.orderid) as order_placed 
from Orders o 
join Customers c on c.CustomerId=o.CustomerId 
group by c.CustomerId,c.FirstName,c.LastName 
order by order_placed desc