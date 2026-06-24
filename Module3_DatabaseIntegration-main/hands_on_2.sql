USE college_db;

INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year) VALUES
('Nisha', 'Kapoor', 'nisha.kapoor@college.edu', '2003-06-15', 2, 2022),
('Rahul', 'Joshi', 'rahul.joshi@college.edu', '2004-02-10', 3, 2023);

SELECT COUNT(*) AS total_students FROM students;

UPDATE enrollments
SET grade = 'B'
WHERE student_id = 5 AND course_id = 1;

SELECT * FROM enrollments WHERE student_id = 5;

SELECT * FROM enrollments WHERE grade IS NULL;

SET SQL_SAFE_UPDATES = 0;

DELETE FROM enrollments WHERE grade IS NULL;

SELECT COUNT(*) AS total_enrollments FROM enrollments;

SELECT student_id, first_name, last_name, email, enrollment_year
FROM students
WHERE enrollment_year = 2022
ORDER BY last_name ASC;

SELECT course_id, course_name, course_code, credits
FROM courses
WHERE credits > 3
ORDER BY credits DESC;

SELECT professor_id, prof_name, email, salary
FROM professors
WHERE salary BETWEEN 80000 AND 95000;

SELECT student_id, first_name, last_name, email
FROM students
WHERE email LIKE '%@college.edu';

SELECT enrollment_year, COUNT(*) AS student_count
FROM students
GROUP BY enrollment_year
ORDER BY enrollment_year;

SELECT CONCAT(s.first_name, ' ', s.last_name) AS full_name, d.dept_name
FROM students s
INNER JOIN departments d ON s.department_id = d.department_id
ORDER BY full_name;

SELECT e.enrollment_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name,
c.course_name, e.enrollment_date, e.grade
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses c ON e.course_id = c.course_id
ORDER BY e.enrollment_id;

SELECT s.student_id, CONCAT(s.first_name, ' ', s.last_name) AS full_name, s.email
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
WHERE e.enrollment_id IS NULL;

SELECT c.course_id, c.course_name, c.course_code, COUNT(e.enrollment_id) AS enrolled_count
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code
ORDER BY enrolled_count DESC;

SELECT d.dept_name, p.prof_name, p.salary
FROM departments d
LEFT JOIN professors p ON d.department_id = p.department_id
ORDER BY d.dept_name, p.salary DESC;

SELECT c.course_name, COUNT(e.enrollment_id) AS enrollment_count
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_name
ORDER BY enrollment_count DESC;

SELECT d.dept_name, ROUND(AVG(p.salary), 2) AS avg_salary
FROM departments d
INNER JOIN professors p ON d.department_id = p.department_id
GROUP BY d.dept_name
ORDER BY avg_salary DESC;

SELECT dept_name, budget
FROM departments
WHERE budget > 600000
ORDER BY budget DESC;

SELECT e.grade, COUNT(*) AS grade_count
FROM enrollments e
INNER JOIN courses c ON e.course_id = c.course_id
WHERE c.course_code = 'CS101'
GROUP BY e.grade
ORDER BY e.grade;

SELECT d.dept_name, COUNT(DISTINCT e.student_id) AS enrolled_students
FROM departments d
INNER JOIN courses c ON d.department_id = c.department_id
INNER JOIN enrollments e ON c.course_id = e.course_id
GROUP BY d.dept_name
HAVING COUNT(DISTINCT e.student_id) > 2
ORDER BY enrolled_students DESC;