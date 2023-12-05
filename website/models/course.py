from website import mysql

class Course(object):
    def __init__(self, code=None, name=None, college=None):
        self.code = code
        self.name = name
        self.college = college

    def add(self):
        cur = mysql.connection.cursor()

        sql = f"INSERT INTO courses (code, name, college) VALUES ('{self.code}','{self.name}','{self.college}')"
        cur.execute(sql)
        mysql.connection.commit()
        cur.close()

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM courses"
        cursor.execute(sql)
        results = cursor.fetchall()

        courses = [cls(code=row[0], name=row[1], college=row[2]) for row in results]
        cursor.close()
        return courses
    
    def show(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM courses ORDER BY code DESC LIMIT 5")
        courses = cur.fetchall()
        return courses
    
    def search(key):
        cur = mysql.connection.cursor()
        corquery = f"SELECT * FROM courses WHERE code LIKE '{key}' OR name LIKE '%{key}%' OR college LIKE '%{key}%'"
        cur.execute(corquery)
        results = cur.fetchall()
        return results
    
    def check_college(college):
        cur = mysql.connection.cursor()
        cur.execute("SELECT code FROM colleges WHERE code = %s", (college,))
        col = cur.fetchone()
        return col

    def check_code(code):
        cur = mysql.connection.cursor()
        cur.execute("SELECT code FROM courses WHERE code = %s", (code,))
        code = cur.fetchone()

        return code

    def delete(self):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE from courses where code = '{self.code}'"
            cursor.execute(sql)
            mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False
        
    def edit(self):
        try:
            cursor = mysql.connection.cursor()
            sql = f"UPDATE courses SET name = '{self.name}', college = '{self.college}' WHERE code = '{self.code}'"
            cursor.execute(sql)
            mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False
        
    def editcode(self, newcode):
        try:
            cursor = mysql.connection.cursor()
            sql = f"UPDATE courses SET code = '{newcode}' WHERE code = '{self.code}'"
            cursor.execute(sql)
            mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False