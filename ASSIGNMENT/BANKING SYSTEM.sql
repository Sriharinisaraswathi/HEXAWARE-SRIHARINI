create database HMBank;
use HMBank;

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY IDENTITY(1,1),
    first_name NVARCHAR(50) NOT NULL,
    last_name NVARCHAR(50) NOT NULL,
    DOB DATE NOT NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    phone_number NVARCHAR(15) UNIQUE,
    address NVARCHAR(255)
);

CREATE TABLE Accounts (
    account_id INT PRIMARY KEY IDENTITY(1000,1),
    customer_id INT NOT NULL,
    account_type NVARCHAR(20) CHECK (account_type IN ('savings', 'current', 'zero_balance')),
    balance DECIMAL(18,2) DEFAULT 0.0,

    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY IDENTITY(100000,1),
    account_id INT NOT NULL,
    transaction_type NVARCHAR(20) CHECK (transaction_type IN ('deposit', 'withdrawal', 'transfer')),
    amount DECIMAL(18,2) NOT NULL CHECK (amount > 0),
    transaction_date DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO Customers (first_name, last_name, DOB, email, phone_number, address)
VALUES
('Amit', 'Sharma', '1985-05-20', 'amit.sharma@example.com', '9876543210', 'Delhi, India'),
('Priya', 'Verma', '1990-11-10', 'priya.verma@example.com', '9876501234', 'Mumbai, India'),
('Rahul', 'Kumar', '1988-01-15', 'rahul.kumar@example.com', '9823456789', 'Chennai, India'),
('Sneha', 'Iyer', '1995-06-25', 'sneha.iyer@example.com', '9812345678', 'Bangalore, India'),
('Ravi', 'Patel', '1992-08-12', 'ravi.patel@example.com', '9900112233', 'Ahmedabad, India'),
('Anjali', 'Nair', '1987-09-18', 'anjali.nair@example.com', '9988776655', 'Kochi, India'),
('Karan', 'Singh', '1993-03-30', 'karan.singh@example.com', '9876123450', 'Noida, India'),
('Divya', 'Kapoor', '1991-12-05', 'divya.kapoor@example.com', '9865432100', 'Pune, India'),
('Vikas', 'Rao', '1986-04-14', 'vikas.rao@example.com', '9845671234', 'Hyderabad, India'),
('Neha', 'Jain', '1994-07-21', 'neha.jain@example.com', '9832123456', 'Jaipur, India');


INSERT INTO Accounts (customer_id, account_type, balance)
VALUES
(1, 'savings', 25000.00),
(2, 'current', 50000.00),
(3, 'zero_balance', 1000.00),
(4, 'savings', 15000.00),
(5, 'current', 70000.00),
(6, 'zero_balance', 0.00),
(7, 'savings', 30000.00),
(8, 'current', 45000.00),
(9, 'savings', 35000.00),
(10, 'zero_balance', 500.00);

INSERT INTO Transactions (account_id, transaction_type, amount, transaction_date)
VALUES
(1000, 'deposit', 5000.00, '2025-04-01 10:00:00'),
(1001, 'withdrawal', 2000.00, '2025-04-02 11:15:00'),
(1002, 'deposit', 1000.00, '2025-04-02 12:30:00'),
(1003, 'withdrawal', 500.00, '2025-04-03 09:45:00'),
(1004, 'transfer', 10000.00, '2025-04-03 14:00:00'),
(1005, 'deposit', 200.00, '2025-04-04 08:00:00'),
(1006, 'withdrawal', 1000.00, '2025-04-04 17:30:00'),
(1007, 'transfer', 2500.00, '2025-04-05 10:15:00'),
(1008, 'deposit', 3000.00, '2025-04-06 16:45:00'),
(1009, 'withdrawal', 400.00, '2025-04-06 19:00:00');

select * from Customers
select * from Accounts
select * from Transactions

--1Write a SQL query to retrieve the name, account type and email of all customers

select a.account_type,
CONCAT(c.first_name,' ',c.last_name) as customername,
c.email from Customers c join Accounts a on c.customer_id=a.customer_id

--2Write a SQL query to list all transaction corresponding customer.

select  CONCAT(c.first_name,' ',c.last_name) as customername ,
t.transaction_type  from Transactions t join Accounts a on a.account_id=t.account_id 
join customers c on c.customer_id =a.customer_id

--3Write a SQL query to increase the balance of a specific account by a certain amount.

update Accounts set balance=balance+100 where account_id=1006
select * from Accounts

--4SQL query to Combine first and last names of customers as a full_name.

select CONCAT(c.first_name,' ',c.last_name) as fullname from Customers c

--5Write a SQL query to remove accounts with a balance of zero where the account type is savings.

delete FROM Accounts
WHERE balance = 0.00 AND account_type = 'savings';
select * from Accounts

--6.Write a SQL query to Find customers living in a specific city.

select customer_id,
concat(first_name,'',last_name) as customername from Customers where  address like '%Kochi%'

--7.Write a SQL query to Get the account balance for a specific account.

select customer_id,
balance from Accounts where account_id=1000;

--8.SQL query to List all current accounts with a balance greater than $1,000.

select customer_id,account_type from Accounts where account_type='current'and balance>1000

--9.Write a SQL query to Retrieve all transactions for a specific account.

select transaction_id,transaction_type from Transactions where account_id=1003

--10.Write a SQL query to Calculate the interest accrued on savings accounts based on a given interest rate.

update Accounts set balance = balance*1.10 where account_type='savings'
select account_id,balance from Accounts

--11.Write a SQL query to Identify accounts where the balance is less than a specified overdraft limit.

select account_id,customer_id,balance from Accounts where balance < -1000;

--12.Write a SQL query to Find customers not living in a specific city.

select customer_id,CONCAT(first_name,' ',last_name) as customername from Customers where address not like '%kochi%';

--TASK 3
--1.Write a SQL query to Find the average account balance for all customers.
select CONCAT(c.first_name,' ',c.last_name)as customer,
avg(a.balance) as averagebalance 
from customers c join Accounts a on c.customer_id=a.customer_id
group by c.first_name,c.last_name
order by averagebalance desc

--2.Write a SQL query to Retrieve the top 10 highest account balances.

select top 10 balance ,
customer_id from Accounts 
order by balance desc

--3.Write a SQL query to Calculate Total Deposits for All Customers in specific date.

select CONCAT(c.first_name,' ',c.last_name)as customer
,sum(t.amount) as total_deposit
from Transactions t join Accounts a on a.account_id=t.account_id 
join Customers c on c.customer_id=a.customer_id 
where cast (t.transaction_date as DATE)='2025-04-04'
group by c. first_name,c.last_name
order by total_deposit desc;

--4.Write a SQL query to Find the Oldest and Newest Customers.

SELECT CONCAT(first_name,' ',last_name)as customer 
FROM Customers
WHERE DOB = (SELECT MIN(DOB) FROM Customers);

SELECT CONCAT(first_name,' ',last_name)as customer 
FROM Customers
WHERE DOB = (SELECT MAX(DOB)  FROM Customers);

--5 a SQL query to Retrieve transaction details along with the account type.
select  t.transaction_id,
t.transaction_type,
a.account_type,
t.transaction_date from Transactions t join Accounts a on a.account_id=t.account_id  
order by t.transaction_date asc;

--6.Write a SQL query to Get a list of customers along with their account details.

select a.account_id,c.customer_id,
CONCAT(c.first_name,' ',c.last_name)as customer,
a.account_type from Accounts a join Customers c on c.customer_id=a.customer_id 
order by a.account_id ;

--7. Write a SQL query to Retrieve transaction details along with customer information for specfic account
select CONCAT(c.first_name,' ',c.last_name)as customer,
c.email,
c.phone_number,
c.address,
t.transaction_type,
t.transaction_date from Transactions t join Accounts a on a.account_id=t.account_id
join Customers c on a.customer_id=c.customer_id 
where a.account_id=1006 
order by a.account_id asc;

--8.Write a SQL query to Identify customers who have more than one account.
 select CONCAT(c.first_name,' ',c.last_name)as customer,
 count(a.account_id) as total_accounts 
 from Customers c join Accounts a on c.customer_id=a.customer_id
 group by c.first_name,c.last_name
 having count(a.account_id) > 1 ;
 
 --9.Write a SQL query to Calculate the difference in transaction amounts between deposits and withdrawals.
SELECT 
    SUM(case when transaction_type = 'deposit' then amount else 0 END) as total_deposit,
    SUM(case when transaction_type = 'withdrawal' then amount else 0 END) as total_withdrawal,
    SUM(case when transaction_type = 'deposit' then amount else 0 END) - 
    SUM(case when transaction_type = 'withdrawal' then amount else 0 END) as difference
FROM Transactions;
--10.SQL query to Calculate the average daily balance for each account over a specified period.
SELECT 
    a.account_id,
    a.customer_id,
    a.balance AS current_balance,
    DATEDIFF(DAY, '2025-04-01', '2025-04-05') + 1 AS total_days,
	CAST(a.balance AS DECIMAL(18,2)) / (DATEDIFF(DAY, '2025-04-01', '2025-04-05') + 1)
FROM Accounts a
ORDER BY a.customer_id;

--11.Calculate the total balance for each account type.

select sum(balance) as total_balance ,
account_type from Accounts 
group by account_type;

--12.Identify accounts with the highest number of transactions order by descending order

select t.account_id,
CONCAT(c.first_name,' ',c.last_name)as customer,
count(t.transaction_id) as total_transactions from transactions t join Accounts a on a.account_id=t.account_id
join Customers c on c.customer_id=a.customer_id
group by c.first_name,c.last_name,t.account_id 
order by total_transactions desc;

--13.List customers with high aggregate account balances, along with their account types.

select CONCAT(c.first_name,' ',c.last_name)as customer,sum(a.balance) as high_balance,a.account_type 
from Accounts a join Customers c on c.customer_id=a.customer_id 
group by c.first_name,c.last_name,a.account_type 
order by high_balance desc;

--14 Identify and list duplicate transactions based on transaction amount, date, and account

SELECT 
 t.transaction_id,
 t.account_id,
 t.amount,
 t.transaction_date,
 t.transaction_type
FROM  Transactions t
JOIN (
    SELECT  amount,transaction_date,account_id,COUNT(*) AS duplicate_count
    FROM Transactions
    GROUP BY 
amount,
transaction_date,
account_id
HAVING COUNT(*) > 1
) dup 
ON 
 t.amount = dup.amount AND t.transaction_date = dup.transaction_date AND t.account_id = dup.account_id
ORDER BY 
    t.account_id, 
    t.transaction_date;

--TASK 4

--1.Retrieve the customer(s) with the highest account balance

select top 1
CONCAT(c.first_name,' ',c.last_name)as customer,a.balance 
from Customers c 
join accounts a  ON  a.customer_id=c.customer_id  
order by a.balance desc;

--2.Calculate the average account balance for customers who have more than one account.

select CONCAT(c.first_name,' ',c.last_name)as customer,
AVG(a.balance) as average_balance
from Accounts a
join Customers c on c.customer_id=a.customer_id
group by c.first_name,c.last_name  
having count(a.account_id) > 1
order by average_balance ;

--3.Retrieve accounts with transactions whose amounts exceed the average transaction amount.

select account_id, amount 
from Transactions  
where amount > (select AVG(amount) from Transactions);

--4.Identify customers who have no recorded transactions.

select CONCAT(c.first_name,' ',c.last_name)as customer 
from Customers c 
join Accounts a on a.customer_id=c.customer_id 
join Transactions t on a.account_id=t.account_id
where t.transaction_id is null;

--5.Calculate the total balance of accounts with no recorded transactions.

select a.account_id,avg(a.balance) as avgbalance 
from Accounts a left join Transactions t  on a.account_id=t.account_id
where transaction_id is null
group by a.account_id;

--6. Retrieve transactions for accounts with the lowest balance.

Select top 1 a.account_id,t.transaction_id,a.balance 
from Accounts a 
left join Transactions t on t.account_id=a.account_id 
order by a.balance asc;

--7.Identify customers who have accounts of multiple types.

select CONCAT(c.first_name,' ',c.last_name)as customer 
from Customers c 
left join Accounts a on a.customer_id=c.customer_id  
group by c.first_name,c.last_name 
having count(distinct a.account_type)>1;

--8.Calculate the percentage of each account type out of the total number of accounts

select account_type,
count(*) as account_count,
cast(count(*)*100.00 / (select count(*) from Accounts) as decimal (10,2)) as percentage
from Accounts 
group by account_type;

--9.Retrieve all transactions for a customer with a given customer_id.

select t.transaction_id,
a.account_id,
CONCAT(c.first_name,' ',c.last_name)as customer,
t.transaction_type 
from Transactions t 
left join Accounts a on t.account_id=a.account_id
join  Customers c on c.customer_id=a.customer_id
where c.customer_id=6  
order by a.account_id,t.transaction_id;

--10.Calculate the total balance for each account type, including a subquery within the SELECT clause.

select distinct account_type , 
(select sum(balance) from Accounts) as total_balance 
from Accounts;







