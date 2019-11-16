import mysql.connector


class StudentManagementSystem:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aa123asd4567+",
            database="sm"
        )

        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(
            "CREATE TABLE IF NOT EXISTS students (student_id INT AUTO_INCREMENT PRIMARY KEY, student_name VARCHAR(50) NOT NULL, student_email VARCHAR(255) NOT NULL)")
        self.mycursor.execute(
            "CREATE TABLE IF NOT EXISTS courses (course_id INT AUTO_INCREMENT PRIMARY KEY, course_name VARCHAR(50) NOT NULL, course_description VARCHAR(255) NOT NULL, course_schedule VARCHAR(255) NOT NULL)")
        self.mycursor.execute(
            "CREATE TABLE IF NOT EXISTS students_courses (student_id INT NOT NULL, course_id INT NOT NULL,CONSTRAINT students_courses_fk_students FOREIGN KEY (student_id) REFERENCES students (student_id),  CONSTRAINT students_courses_fk_courses FOREIGN KEY (course_id) REFERENCES courses (course_id))")

    def addStudent(self, student_name, student_email):
        sql = "INSERT INTO students VALUES (DEFAULT,%s, %s)"
        self.mycursor.execute(sql, (student_name, student_email))
        self.mydb.commit()

    def addCourse(self, course_name, course_description, days):
        course_day = ','.join(days)
        sql = "INSERT INTO courses VALUES (DEFAULT,%s, %s, %s)"
        self.mycursor.execute(
            sql, (course_name, course_description, course_day))
        self.mydb.commit()

    def enrollToCourse(self, student_id, course_id):
        if self.alreadyEnroll(student_id, course_id):
            return 1
        elif len(self.getStudentByID(student_id)) == 0:
            return 2
        elif len(self.getCourseByID(course_id)) == 0:
            return 3
        sql = "INSERT INTO students_courses VALUES (%s, %s)"
        self.mycursor.execute(sql, (student_id, course_id))
        self.mydb.commit()
        return 0

    def getStudentByID(self, student_id):
        sql = "SELECT * FROM students WHERE student_id = %s"
        self.mycursor.execute(sql, (student_id,))
        res = self.mycursor.fetchall()
        return res

    def getCourseByID(self, course_id):
        sql = "SELECT * FROM courses WHERE course_id = %s"
        self.mycursor.execute(sql, (course_id,))
        res = self.mycursor.fetchall()
        return res

    def alreadyEnroll(self, student_id, course_id):
        sql = "SELECT * FROM students_courses s WHERE s.student_id = %s and s.course_id = %s"
        self.mycursor.execute(sql, (student_id, course_id))
        res = self.mycursor.fetchall()
        return len(res) > 0

    def getAllStudentsByCourseID(self, course_id):
        if len(self.getCourseByID(course_id)) == 0:
            return []
        sql = "SELECT s.student_name FROM courses c JOIN students_courses sc ON c.course_id = sc.course_id JOIN students s ON sc.student_id = s.student_id WHERE c.course_id = %s ORDER BY s.student_name"
        self.mycursor.execute(sql, (course_id,))
        res = self.mycursor.fetchall()
        return [r[0] for r in res]

    def getAllCoursesByStudentID(self, student_id):
        if len(self.getStudentByID(student_id)) == 0:
            return []
        sql = "SELECT c.course_name FROM courses c JOIN students_courses sc ON c.course_id = sc.course_id JOIN students s ON sc.student_id = s.student_id WHERE s.student_id = %s ORDER BY c.course_name"
        self.mycursor.execute(sql, (student_id,))
        res = self.mycursor.fetchall()
        return [r[0] for r in res]

    def getAllCoursesByStudentIDOnOneDay(self, student_id, day):
        if len(self.getStudentByID(student_id)) == 0:
            return []
        sql = "SELECT c.course_name FROM courses c JOIN students_courses sc ON c.course_id = sc.course_id JOIN students s ON sc.student_id = s.student_id WHERE s.student_id = %s and c.course_schedule LIKE %s ORDER BY c.course_name"
        self.mycursor.execute(sql, (student_id, '%'+day+'%'))
        res = self.mycursor.fetchall()
        return [r[0] for r in res]

    def close(self):
        self.mycursor.close()
        self.mydb.close()


def test():
    sm = StudentManagementSystem()
    # for i in range(10):
    #     sm.addStudent('student'+str(i), 's'+str(i)+'@uci.edu')
    # sm.addCourse('Algorithm', 'SWE 241P, EASY', ['Mon', 'Tue', 'Wes'])
    # sm.addCourse('Network', 'SWE 242P, EASY', ['Mon', 'Tue', 'Wes'])
    # sm.addCourse('Database', 'SWE 243P, EASY', ['Wes'])
    # sm.addCourse('Concurrency', 'SWE 244P, EASY', ['Tue', 'Wes', 'Fri'])
    # print(sm.enrollToCourse(2, 1))
    # print(sm.enrollToCourse(2, 2))
    # print(sm.enrollToCourse(2, 3))
    # print(sm.enrollToCourse(2, 4))
    # print(sm.enrollToCourse(5, 3))
    # print(sm.enrollToCourse(5, 4))
    # print(sm.getAllStudentsByCourseID(1))
    # print(sm.getAllStudentsByCourseID(2))
    # print(sm.getAllStudentsByCourseID(20))
    # print(sm.getAllCoursesByStudentID(3))
    # print(sm.getAllStudentsByCourseID(4))
    # print(sm.getAllStudentsByCourseID(5))
    # print(sm.getAllStudentsByCourseID(20))
    print(sm.getAllCoursesByStudentIDOnOneDay(1, 'Mon'))
    sm.close()


def main():
    sm = StudentManagementSystem()
    while True:
        print("----------------------\n" +
              "Welcome to student enrollment system:\n" +
              "1. Add a student\n" +
              "2. Add a course\n" +
              "3. Enroll\n"
              "4. Find a student's courses\n" +
              "5. Find all students in a specific course\n" +
              "6. Check schedule for a student on a day\n" +
              "7. Exit")

        command = input()
        if command == '1':
            name = input('Please Input the Student Name: ')
            email = input('Please Input the Student Email: ')
            sm.addStudent(name, email)
            print('Add Student Successfully!\n')
        elif command == '2':
            name = input('Please Input the Course Name: ')
            description = input('Please Input the Course Description: ')
            schedule = input('Please Input the Course Schedule: ')
            sm.addCourse(name, description, schedule.split(' '))
            print('Add Course Successfully!\n')
        elif command == '3':
            sid = input('Please Input the Student ID: ')
            cid = input('Please Input the Course ID: ')
            res = sm.enrollToCourse(sid, cid)
            if res == 0:
                print('Enroll Successfully!\n')
            elif res == 1:
                print('Already Enrolled.\n')
            elif res == 2:
                print('Student No Found.\n')
            elif res == 3:
                print('Course No Found.\n')

        elif command == '4':
            sid = input('Please Input the Student ID: ')
            res = sm.getAllCoursesByStudentID(sid)
            if res:
                print('Search Successfully!\n')
                print(res)
                print('\n')
            else:
                print('Student No Found.\n')
        elif command == '5':
            cid = input('Please Input the Course ID: ')
            res = sm.getAllStudentsByCourseID(cid)
            if res:
                print('Search Successfully!\n')
                print(res)
                print('\n')
            else:
                print('Course No Found.\n')
        elif command == '6':
            cid = input('Please Input the Student ID: ')
            day = input('Please Input the Day You Want to Check: ')
            res = sm.getAllCoursesByStudentIDOnOneDay(sid, day)
            if res:
                print('Search Successfully!\n')
                print(res)
                print('\n')
            else:
                print('No Data')
        elif command == '7':
            print('Thank you!')
            return
        else:
            print('Invalid Input!\n')


if __name__ == "__main__":
    # test()
    main()
