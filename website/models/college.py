from website import mysql

class College(object):
    def __init__(self, code=None, name=None):
        self.code = code
        self.name = name

    def add(self):
        cur = mysql.connection.cursor()

        sql = f"INSERT INTO colleges (code, name) VALUES ('{self.code}','{self.name}')"
        cur.execute(sql)
        mysql.connection.commit()
        cur.close()

    @classmethod
    def all(cls):
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM colleges"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def show(self):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM colleges ORDER BY code DESC LIMIT 5")
        colleges = cur.fetchall()
        return colleges
    
    def search(key):
        cur = mysql.connection.cursor()
        colquery = f"SELECT * FROM colleges WHERE code LIKE '{key}' OR name LIKE '%{key}%'"
        cur.execute(colquery)
        results = cur.fetchall()
        return results
    

    def delete(self):
        try:
            cursor = mysql.connection.cursor()
            sql = f"DELETE from colleges where code = '{self.code}'"
            cursor.execute(sql)
            mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False
        
    def check_code(code):
        cur = mysql.connection.cursor()
        cur.execute("SELECT code FROM colleges WHERE code = %s", (code,))
        code = cur.fetchone()

        return code
        
    def edit(self):
        try:
            cursor = mysql.connection.cursor()
            sql = f"UPDATE colleges SET name = '{self.name}' WHERE code = '{self.code}'"
            cursor.execute(sql)
            mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False
        
    def editcode(self, new):
        try:
            cursor = mysql.connection.cursor()
            sql = f"UPDATE colleges SET code = '{new}' WHERE code = '{self.code}'"
            cursor.execute(sql)
            mysql.connection.commit()
            cursor.close()
            return True
        except:
            return False