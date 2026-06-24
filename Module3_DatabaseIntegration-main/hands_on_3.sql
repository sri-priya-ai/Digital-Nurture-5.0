USE college_db;

SELECT first_name, last_name
FROM students
WHERE student_id IN (
    SELECT student_id
    FROM enrollments
    WHERE course_id = (
        SELECT course_id
        FROM courses
        WHERE course_code = 'CS101'
    )
);

SELECT first_name, last_name
FROM students
WHERE student_id IN (
    SELECT student_id
    FROM enrollments
    WHERE grade = 'A'
);

SELECT prof_name, salary
FROM professors
WHERE salary = (
    SELECT MAX(salary)
    FROM professors
);

CREATE VIEW student_department_view AS
SELECT s.student_id,
       s.first_name,
       s.last_name,
       d.dept_name
FROM students s
JOIN departments d
ON s.department_id = d.department_id;

SELECT * FROM student_department_view;

CREATE VIEW course_enrollment_view AS
SELECT c.course_name,
       COUNT(e.enrollment_id) AS total_students
FROM courses c
LEFT JOIN enrollments e
ON c.course_id = e.course_id
GROUP BY c.course_name;

SELECT * FROM course_enrollment_view;


DROP PROCEDURE IF EXISTS GetStudentsByDepartment;
DROP PROCEDURE IF EXISTS GetProfessorsBySalary;

DELIMITER //

CREATE PROCEDURE GetStudentsByDepartment(IN dept INT)
BEGIN
    SELECT *
    FROM students
    WHERE department_id = dept;
END //

CREATE PROCEDURE GetProfessorsBySalary(IN min_salary DECIMAL(10,2))
BEGIN
    SELECT prof_name, salary
    FROM professors
    WHERE salary >= min_salary;
END //

DELIMITER ;

CALL GetStudentsByDepartment(1);

CALL GetProfessorsBySalary(80000);

START TRANSACTION;

UPDATE professors
SET salary = salary + 5000
WHERE department_id = 1;

SAVEPOINT salary_update;

UPDATE professors
SET salary = salary + 2000
WHERE department_id = 2;

ROLLBACK TO salary_update;

COMMIT;

SELECT * FROM professors;

SHOW PROCEDURE STATUS;

SHOW FULL TABLES
WHERE Table_type = 'VIEW';