import sqlite3
from student import Student


class StudentExerciseReports():

    """Methods for reports on the Student Exercises database"""

    def __init__(self):
        # Contains the absolute path to your database file
        self.db_path = "/Users/jdavid/Projects/nss/c38/workspace/sql/python-sql/studentexercises.db"

    # def create_student(self, cursor, row):
    #     return Student(row[1], row[2], row[3], row[5])

    def all_students(self):
        """Retrieve all students with the cohort name"""

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = lambda cursor, row: Student(
                row[1], row[2], row[3], row[5])
            # conn.row_factory = lambda cursor, row: Student(*row)

            db_cursor = conn.cursor()

            execute_query = db_cursor.execute("""
            SELECT s.Id,
                s.FirstName,
                s.LastName,
                s.SlackHandle,
                s.CohortId,
                c.Name
            FROM Student s
            JOIN Cohort c ON s.CohortId = c.Id
            ORDER BY s.CohortId
            """)

            # print(execute_query)

            all_students = db_cursor.fetchall()

            # print(all_students)

            # When there is no row_factory function defined, we get a list of tuples
            # for student in all_students:
            #     print(f'{student[1]} {student[2]} is in {student[5]}')

            # We have a row_factory function specified. That lambda takes each tuple and returns an instance of the Student class
            for student in all_students:
                print(
                    f'{student.first_name} {student.last_name} is in {student.cohort}')

            # db_cursor.execute("SELECT i.FirstName, i.LastName FROM Instructor i")

            # all_instructors = db_cursor.fetchall()

            # print(all_instructors)


reports = StudentExerciseReports()
reports.all_students()
