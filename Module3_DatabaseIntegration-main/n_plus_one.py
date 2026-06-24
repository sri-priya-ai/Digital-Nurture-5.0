import mysql.connector
import time

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sripriya@26072005",
    database="college_db"
)

db_cursor = connection.cursor()

start_time = time.time()

total_queries = 1

db_cursor.execute("SELECT student_id, first_name, last_name FROM students")
students = db_cursor.fetchall()

for student in students:
    student_id = student[0]

    db_cursor.execute(
        "SELECT course_name FROM courses c "
        "JOIN enrollments e ON c.course_id = e.course_id "
        "WHERE e.student_id = %s",
        (student_id,)
    )

    courses = db_cursor.fetchall()
    total_queries += 1

    print(student[1], student[2], ":", courses)

end_time = time.time()

print("\nDatabase queries used :", total_queries)
print("Execution time :", round(end_time - start_time, 6), "seconds")

connection.close()