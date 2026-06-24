USE college_db;

DROP INDEX idx_students_enrollment_year ON students;
DROP INDEX idx_enrollment_student_course ON enrollments;

CREATE INDEX idx_students_enrollment_year
ON students(enrollment_year);

CREATE INDEX idx_enrollment_student_course
ON enrollments(student_id, course_id);

SHOW INDEX FROM students;
SHOW INDEX FROM enrollments;

EXPLAIN
SELECT *
FROM students
WHERE enrollment_year = 2022;

EXPLAIN
SELECT s.first_name,
       s.last_name,
       c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

SELECT s.first_name,
       s.last_name,
       c.course_name
FROM enrollments e
JOIN students s
ON s.student_id = e.student_id
JOIN courses c
ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

SHOW STATUS LIKE 'Handler_read%';

ANALYZE TABLE students;
ANALYZE TABLE enrollments;
ANALYZE TABLE courses;

SHOW TABLE STATUS;

EXPLAIN
SELECT *
FROM enrollments
WHERE student_id = 1
AND course_id = 1;

SELECT *
FROM enrollments
WHERE student_id = 1
AND course_id = 1;