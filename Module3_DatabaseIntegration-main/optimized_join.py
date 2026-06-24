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

sql_query = """
SELECT
    CONCAT(s.first_name, ' ', s.last_name) AS student_name,
    c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
"""

db_cursor.execute(sql_query)

result = db_cursor.fetchall()

print("------ Optimized JOIN Version ------")

for row in result:
    print(row)

print("\nDatabase queries used : 1")
print("Rows fetched :", len(result))

end_time = time.time()

print("Execution time :", round(end_time - start_time, 6), "seconds")

connection.close()