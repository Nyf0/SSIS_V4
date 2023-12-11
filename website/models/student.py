from website import mysql
import re

class Student(object):
    def __init__(self, id=None, pic=None, fname=None, lname=None, course=None, gender=None, level=None):
        self.id = id
        self.pic = pic
        self.fname = fname
        self.lname = lname
        self.course = course
        self.gender = gender
        self.level = level

    def add(self):
        cur = mysql.connection.cursor()

        sql = "INSERT INTO students (student_id, pic, fname, lname, course, gender, level) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (self.id, self.pic, self.fname, self.lname, self.course, self.gender, self.level)

        cur.execute(sql, values)
        mysql.connection.commit()
        cur.close()

    def show(self):
        cur = mysql.connection.cursor()
        sql = f"SELECT * FROM students ORDER BY student_id DESC LIMIT 5"
        cur.execute(sql)
        students = cur.fetchall()
        cur.close()
        return students
    
    def get():
        cur = mysql.connection.cursor()
        cur.execute("SELECT students.pic, students.student_id, students.fname, students.lname, students.course, students.gender, students.level, colleges.code, colleges.name FROM students INNER JOIN courses ON students.course = courses.code INNER JOIN colleges ON courses.college = colleges.code")
        Students = cur.fetchall()
        cur.close()
        return Students
    
    def search(key):
        cur = mysql.connection.cursor()
        studquery = f"SELECT students.student_id, students.fname, students.lname, students.course, students.gender, students.level, colleges.code, colleges.name, students.pic FROM students INNER JOIN courses ON students.course = courses.code INNER JOIN colleges ON courses.college = colleges.code WHERE students.student_id = '{key}' OR students.fname LIKE '%{key}%' OR students.lname LIKE '%{key}%' OR students.course = '{key}' OR students.gender = '{key}' OR students.level = '{key}' OR colleges.code = '{key}' OR colleges.name LIKE '{key}'"
        cur.execute(studquery)
        results = cur.fetchall()
        cur.close()
        return results
    
    def fetch(id):
        cur = mysql.connection.cursor()
        query = "SELECT * FROM students WHERE student_id = %s"
        cur.execute(query,(id,))
        stud = cur.fetchone()
        cur.close()

        return stud
    
    def view(id):
        cur = mysql.connection.cursor()
        query = """
            SELECT students.*, courses.name AS course_name, colleges.code AS college_code, colleges.name AS college_name 
            FROM students 
            JOIN courses ON students.course = courses.code 
            JOIN colleges ON courses.college = colleges.code 
            WHERE students.student_id = %s;
        """
        cur.execute(query, (id,))
        student = cur.fetchone()
        cur.close()
        return student


    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * from students"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def check_course(course):
        cur = mysql.connection.cursor()
        cur.execute("SELECT code FROM courses WHERE code = %s", (course,))
        cor = cur.fetchone()
        cur.close()
        return cor
    
    def check_id(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT student_id FROM students WHERE student_id = %s", (id,))
        ids = cur.fetchone()
        cur.close()
        return ids

    def delete(self):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE from students where student_id= '{self.id}'"
            cursor.execute(sql)
            mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False
        
    def edit(self, old_id):
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE students SET student_id = %s, pic = %s, fname = %s, lname = %s, course = %s, gender = %s, level = %s WHERE student_id = %s"
            cursor.execute(sql,(self.id,self.pic,self.fname,self.lname,self.course,self.gender,self.level,old_id,))
            mysql.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(e)
            return False
        
    def edit_without(self, old_id):
        try:
            cursor = mysql.connection.cursor()
            sql = "UPDATE students SET student_id = %s, fname = %s, lname = %s, course = %s, gender = %s, level = %s WHERE student_id = %s"
            cursor.execute(sql,(self.id,self.fname,self.lname,self.course,self.gender,self.level,old_id,))
            mysql.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(e)
            return False
        
    def get_public_id_from_url(url):
        match = re.search(r'/v\d+/(SSIS/[^/]+)\.\w+', url)  # Updated for the presence of digits after /v

        return match.group(1) if match else None

    def get_pic(id):
        cur = mysql.connection.cursor()
        sql = "SELECT pic FROM students WHERE student_id = %s"
        cur.execute(sql,(id,))
        pic = cur.fetchone()
        cur.close()
        return pic
    

