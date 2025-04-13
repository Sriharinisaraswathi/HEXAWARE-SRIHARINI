create database SISDB;
USE SISDB;

CREATE TABLE Students (
    student_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    email VARCHAR(100),
    phone_number VARCHAR(15)
);

CREATE TABLE Teacher (
    teacher_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100)
);

CREATE TABLE Courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(100),
    credits INT,
    teacher_id INT,
    FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
);

CREATE TABLE Enrollments (
    enrollment_id INT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

CREATE TABLE Payments (
    payment_id INT PRIMARY KEY,
    student_id INT,
    amount DECIMAL(10, 2),
    payment_date DATE,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

INSERT INTO Students (student_id, first_name, last_name, date_of_birth, email, phone_number) VALUES
(1, 'sri', 'harini', '2003-08-24', 'sri.hari@email.com', '9876543220'),
(2, 'Jane', 'Smith', '2001-03-22', 'jane.smith@email.com', '9876543211'),
(3, 'Alice', 'Johnson', '1999-07-08', 'alice.j@email.com', '9876543212'),
(4, 'Bob', 'Brown', '2000-12-10', 'bob.b@email.com', '9876543213'),
(5, 'Eve', 'Davis', '2002-09-25', 'eve.d@email.com', '9876543214'),
(6, 'Charlie', 'Wilson', '2000-05-18', 'charlie.w@email.com', '9876543215'),
(7, 'Grace', 'Lee', '2001-11-05', 'grace.l@email.com', '9876543216'),
(8, 'David', 'Clark', '1998-08-30', 'david.c@email.com', '9876543217'),
(9, 'Sophia', 'Hall', '2003-02-14', 'sophia.h@email.com', '9876543218'),
(10, 'Liam', 'Allen', '1999-06-21', 'liam.a@email.com', '9876543219');

INSERT INTO Teacher (teacher_id, first_name, last_name, email) VALUES
(101, 'Drake', 'Morris', 'drake.m@email.com'),
(102, 'Ella', 'Woods', 'ella.w@email.com'),
(103, 'Olivia', 'Bennett', 'olivia.b@email.com'),
(104, 'Noah', 'Cooper', 'noah.c@email.com'),
(105, 'Mia', 'Gray', 'mia.g@email.com'),
(106, 'Lucas', 'Hughes', 'lucas.h@email.com'),
(107, 'Emma', 'Ward', 'emma.w@email.com'),
(108, 'James', 'Carter', 'james.c@email.com'),
(109, 'Ava', 'Morgan', 'ava.m@email.com'),
(110, 'Benjamin', 'Reed', 'ben.reed@email.com');

INSERT INTO Courses (course_id, course_name, credits, teacher_id) VALUES
(201, 'Data Structures', 4, 101),
(202, 'Database Systems', 3, 102),
(203, 'Operating Systems', 4, 103),
(204, 'Computer Networks', 3, 104),
(205, 'Machine Learning', 4, 105),
(206, 'Cloud Computing', 3, 106),
(207, 'Artificial Intelligence', 4, 107),
(208, 'Cyber Security', 3, 108),
(209, 'Web Development', 3, 109),
(210, 'Mobile App Development', 3, 110);

INSERT INTO Enrollments (enrollment_id, student_id, course_id, enrollment_date) VALUES
(301, 1, 201, '2024-06-01'),
(302, 2, 202, '2024-06-02'),
(303, 3, 203, '2024-06-03'),
(304, 4, 204, '2024-06-04'),
(305, 5, 205, '2024-06-05'),
(306, 6, 206, '2024-06-06'),
(307, 7, 207, '2024-06-07'),
(308, 8, 208, '2024-06-08'),
(309, 9, 209, '2024-06-09'),
(310, 10, 210, '2024-06-10');

INSERT INTO Payments (payment_id, student_id, amount, payment_date) VALUES
(401, 1, 5000, '2024-06-11'),
(402, 2, 4500, '2024-06-12'),
(403, 3, 5200, '2024-06-13'),
(404, 4, 4800, '2024-06-14'),
(405, 5, 5000, '2024-06-15'),
(406, 6, 5300, '2024-06-16'),
(407, 7, 4700, '2024-06-17'),
(408, 8, 4900, '2024-06-18'),
(409, 9, 5100, '2024-06-19'),
(410, 10, 5000, '2024-06-20');

SELECT * FROM students
SELECT * FROM Teacher
SELECT * FROM Courses
SELECT * FROM Enrollments
SELECT * FROM Payments

--TASK 2--
--*1. Write an SQL query to insert a new student into the "Students" table with the following details:

INSERT INTO Students VALUES (011,'John','Doe','1995-08-15','john.doe@example.com',1234567890);
SELECT * FROM Students;

--*2. Write an SQL query to enroll a student in a course. Choose an existing student and course and 
insert a record into the "Enrollments" table with the enrollment date. 

INSERT INTO Enrollments VALUES (11, 7, 8, '2024-10-01')
SELECT * FROM Enrollments;

--*3. Update the email address of a specific teacher in the "Teacher" table. Choose any teacher and modify their email address. 

UPDATE Teacher SET Email='drake.morris@email.com' WHERE last_name='Morris';
SELECT * FROM Teacher;

--4.Write an SQL query to delete a specific enrollment record from the "Enrollments" table. Select an enrollment record based on the student and course.

DELETE  FROM Enrollments where student_id=1 and course_id=201 
select * from Enrollments

--5.Update the "Courses" table to assign a specific teacher to a course. Choose any course and teacher from the respective tables.

UPDATE Courses SET  teacher_id=103 where course_id=204
select * from Courses

--6.Delete a specific student from the "Students" table and remove all their enrollment records from the "Enrollments" table. Be sure to maintain referential integrity.

DELETE FROM Enrollments WHERE student_id=6;
DELETE FROM Payments WHERE student_id=6;
DELETE FROM Students WHERE student_id=6;
SELECT * FROM Students;
SELECT * FROM Enrollments;
SELECT * FROM Payments;

--7.Update the payment amount for a specific payment record in the "Payments" table. Choose any payment record and modify the payment amount.

UPDATE Payments SET amount=4500 WHERE payment_id=401;
SELECT * FROM Payments;

--TASK 3
--1.Write an SQL query to calculate the total payments made by a specific student. You will need to join the "Payments" table with the "Students" table based on the student's ID.

SELECT (s.first_name+' '+s.last_name)AS Student_name,SUM(p.amount) AS Total_payments 
FROM Students s 
JOIN Payments p ON s.student_id=p.student_id 
WHERE s.student_id = 1 
GROUP BY (s.first_name+' '+s.last_name);

--2. Write an SQL query to retrieve a list of courses along with the count of students enrolled in each course. Use a JOIN operation between the "Courses" table and the "Enrollments" table.

SELECT c.course_name, COUNT(e.student_id) AS 'No_of_Students'
FROM Courses c 
LEFT JOIN Enrollments e ON c.course_id=e.course_id
GROUP BY course_name;

--3. Write an SQL query to find the names of students who have not enrolled in any course. Use a LEFT JOIN between the "Students" table and the "Enrollments" table to identify students 
--without enrollments.

SELECT CONCAT(first_name,' ',last_name) AS Student_name FROM Students s 
LEFT JOIN Enrollments e ON s.student_id=e.student_id
WHERE enrollment_id IS NULL;

--4.Write an SQL query to retrieve the first name, last name of students, and the names of the courses they are enrolled in. Use JOIN operations between the "Students" table and the "Enrollments" and "Courses" tables. */

SELECT first_name,last_name,course_name	
FROM Students s
JOIN Enrollments e ON s.student_id=e.student_id
JOIN Courses c ON e.course_id=c.course_id
WHERE enrollment_id IS NOT NULL;

--5--list the names of teachers and the courses they are assigned to. Join the "Teacher" table with the "Courses" table.

SELECT CONCAT(first_name,' ',last_name) AS Teacher_name, course_name
FROM Teachers t 
LEFT JOIN Courses c ON T.teacher_id=c.teacher_id;

--6--list of students and their enrollment dates for a specific course. You'll need to join the "Students" table with the "Enrollments" and "Courses" tables.

SELECT CONCAT(first_name,' ',last_name) AS Student_name, enrollment_date 
FROM Students s 
JOIN Enrollments e ON s.student_id=e.student_id
JOIN Courses c ON e.course_id=c.course_id
WHERE e.course_id=1;

--7--Find the names of students who have not made any payments. Use a LEFT JOIN between the "Students" table and the "Payments" table and filter for students with NULL payment records.

SELECT CONCAT(first_name,' ',last_name) AS Student_name 
FROM Students s 
LEFT JOIN Payments p ON s.student_id=p.student_id
WHERE p.payment_id IS NULL;

--8--Write a query to identify courses that have no enrollments. You'll need to use a LEFT JOIN between the "Courses" table and the "Enrollments" table and filter for courses with NULL enrollment records.

SELECT c.course_name
FROM Courses c 
LEFT JOIN Enrollments e ON c.course_id=e.course_id
WHERE e.enrollment_id IS NULL;

--9--Identify students who are enrolled in more than one course. Use a self-join on the "Enrollments" table to find students with multiple enrollment records.

SELECT s.student_id , CONCAT(first_name,last_name) AS Student_name,COUNT(e.course_id) AS 'No. of courses'
FROM Students s
JOIN Enrollments e ON s.student_id=e.student_id
GROUP BY s.student_id,CONCAT(first_name,last_name)
HAVING COUNT(e.course_id)>1
ORDER BY s.student_id;

--10--Find teachers who are not assigned to any courses. Use a LEFT JOIN between the "Teacher" table and the "Courses" table and filter for teachers with NULL course assignments

SELECT CONCAT(first_name,' ',last_name) AS Teacher_name
FROM Teachers t 
LEFT JOIN Courses c ON T.teacher_id=c.teacher_id
WHERE c.course_id IS NULL;

--TASK 4
--1 Write an SQL query to calculate the average number of students enrolled in each course. Use aggregate functions and subqueries to achieve this.

SELECT AVG(student_count) AS average_enrollments_per_course
FROM (
    SELECT course_id,COUNT(student_id) AS student_count
    FROM  Enrollments
    GROUP BY course_id
) AS course_enrollment_counts;

--2--Identify the student(s) who made the highest payment. Use a subquery to find the maximum payment amount and then retrieve the student(s) associated with that amount.

SELECT p.student_id,CONCAT(first_name,' ',last_name)AS std_name, p.amount
FROM Payments p
JOIN Students s ON p.student_id= s.student_id
WHERE amount = (SELECT MAX (amount) FROM Payments);

--3--Retrieve a list of courses with the highest number of enrollments. Use subqueries to find the course(s) with the maximum enrollment count.

SELECT c.course_name, COUNT(e.student_id) AS enrollment_count
FROM Courses c
JOIN Enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name
HAVING COUNT(e.student_id) = (
    SELECT MAX(course_enrollments)
    FROM (
        SELECT COUNT(student_id) AS course_enrollments
        FROM Enrollments
        GROUP BY course_id
    ) AS max
);

--4--Calculate the total payments made to courses taught by each teacher. Use subqueries to sum payments for each teacher's courses.

SELECT t.first_name, t.last_name, (
    SELECT SUM(p.amount)
    FROM Payments p
    WHERE p.student_id IN (
        SELECT e.student_id
        FROM Enrollments e
        JOIN Courses c ON e.course_id = c.course_id
        WHERE c.teacher_id = t.teacher_id
    )
) AS total_payments
FROM Teachers t;

--5--Identify students who are enrolled in all available courses. Use subqueries to compare a student's enrollments with the total number of courses.

SELECT s.first_name, s.last_name
FROM Students s
WHERE NOT EXISTS (
    SELECT c.course_id
    FROM Courses c
    WHERE c.course_id NOT IN (
        SELECT e.course_id
        FROM Enrollments e
        WHERE e.student_id = s.student_id
    )
);

--6--Retrieve the names of teachers who have not been assigned to any courses. Use subqueries to find teachers with no course assignments.

SELECT first_name, last_name FROM Teachers
WHERE teacher_id NOT IN (
    SELECT teacher_id FROM Courses
    WHERE teacher_id IS NOT NULL
);

--7--Calculate the average age of all students. Use subqueries to calculate the age of each student based on their date of birth.

SELECT AVG(age) AS average_age
FROM (
    SELECT DATEDIFF(YEAR, date_of_birth, GETDATE()) AS age
    FROM Students
) AS sub;

--8--Identify courses with no enrollments. Use subqueries to find courses without enrollment records.

SELECT course_name
FROM Courses
WHERE course_id NOT IN (
    SELECT DISTINCT course_id FROM Enrollments
);

--9--Calculate the total payments made by each student for each course they are enrolled in. Use subqueries and aggregate functions to sum payments.

SELECT CONCAT(s.first_name,' ', s.last_name) AS Std_name, c.course_name, 
(
    SELECT SUM(p.amount)
    FROM Payments p
    WHERE p.student_id = s.student_id
) AS total_payment
FROM Students s
JOIN Enrollments e ON s.student_id = e.student_id
JOIN Courses c ON e.course_id = c.course_id
GROUP BY s.student_id, s.first_name, s.last_name, c.course_name;

--10 Identify students who have made more than one payment. Use subqueries and aggregate 
--functions to count payments per student and filter for those with counts greater than one.

SELECT CONCAT(s.first_name,' ', s.last_name) AS Std_name
FROM Students s
WHERE (
    SELECT COUNT(p.payment_id)
    FROM Payments p
    WHERE p.student_id = s.student_id
) > 1;

--11 calculate the total payments made by each student. Join the "Students" table with the "Payments" table and use GROUP BY to calculate the sum of payments for each student.

SELECT CONCAT(s.first_name,' ', s.last_name) AS Std_name, SUM(p.amount) AS total_payments
FROM Students s
JOIN Payments p ON s.student_id = p.student_id
GROUP BY s.first_name,s.last_name;

--12--Retrieve a list of course names along with the count of students enrolled in each course. Use JOIN operations between the "Courses" table and the "Enrollments" table and GROUP BY to count enrollments.

SELECT c.course_name, COUNT(e.student_id) AS student_count
FROM Courses c
LEFT JOIN Enrollments e ON c.course_id = e.course_id
GROUP BY c.course_name;

--13--Calculate the average payment amount made by students. Use JOIN operations between the "Students" table and the "Payments" table and GROUP BY to calculate the average.

SELECT AVG(student_total) AS avg_payment_per_student
FROM (
    SELECT SUM(p.amount) AS student_total
    FROM Payments p
    GROUP BY p.student_id
) AS std_date;
