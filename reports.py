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

    def exercises_with_students(self):
        with sqlite3.connect(self.db_path) as conn:
            db_cursor = conn.cursor()
            
            exercises = dict()

            db_cursor.execute("""
                select
                    e.Id ExerciseId,
                    e.Name,
                    s.Id,
                    s.FirstName,
                    s.LastName
                from Exercise e
                join StudentExercise se on se.ExerciseId = e.Id
                join Student s on s.Id = se.StudentId
            """)

            dataset = db_cursor.fetchall()
            
            # print("The data coming back from the db", dataset)
            
            # Let's take our list of tuples and convert it to a dictionary with the exercise name as the key and a list of students as the value.
            # exercises = {
            #     "Overly Excited": ["Ryan Tanay", "Kate Williams"],
            #     "ChickenMonkey": ["Juan Rodriguez"],
            #     "Stock Report": ["Juan Rodriguez", "Natasha Cox"],
            #     "Urban Planner": ["Ryan Tanay"],
            #     "Bag o' Loot": ["Juan Rodriguez"]
            # }
            for row in dataset:
                exercise_id = row[0]
                exercise_name = row[1]
                student_id = row[2]
                student_name = f'{row[3]} {row[4]}'
                
                if exercise_name not in exercises:
                    # Add a new key/value pair to the exercises dictionary, where the key is the exercise_name and the value is a list with a single item, the student_name.
                    exercises[exercise_name] = [student_name]
                else:
                    # Since the exercise_name alreadys exists as a key in the dictionary, we get the value for that key, which is a list and add the student_name to the end of that list.
                    exercises[exercise_name].append(student_name)
                # print("The dictionary of exercises", exercises)
                
                
            # The output we want to display is:
            # Overly Excited
            #     * Ryan Tanay
            #     * Kate Williams

            # ChickenMonkey
            #     * Juan Rodriguez

            # Stock Report
            #     * Juan Rodriguez

            # Urban Planner
            #     * Ryan Tanay
            #     * Natasha Cox

            # Bag o' Loot
            #     * Juan Rodriguez
            for exercise_name, students in exercises.items():
                print(exercise_name)
                for student in students:
                    print(f'\t* {student}')


reports = StudentExerciseReports()

print("*** A list of students ***")
reports.all_students()

print("*** A list of exercises and the students working on each exercise ***")
reports.exercises_with_students()
