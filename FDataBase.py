import sqlite3
from flask import Flask, jsonify, request

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()







#Редактирование пользователя

    def update(self,Login,p,id_user,FullName,Password):
        faf = p

        try:
            if faf == 'Update':
             self.__cur.execute(f"UPDATE Users set Login = ?,FullName=?,Password=? WHERE id_user = ?",(Login,FullName,Password,id_user,))
             self.__db.commit()
             print('Пользователь %s успешно отредактирован' % (Login))
            elif faf == 'Delete':
                self.__cur.execute(f"DELETE FROM Users where Login = ?", (Login,))
                self.__db.commit()
                print('Пользователь %s спешно удален' % (Login))

        except sqlite3.Error as e:
            print("Ошибка" + str(e))
            return False
        return True



#Для поиска
    def getUsersFromSearch(self,search):
        try:
            if search == "":
                self.__cur.execute("SELECT * FROM Users")
                res = self.__cur.fetchall()
                if res: return res


            else:
                 self.__cur.execute("SELECT * FROM Users WHERE ((Login = ?) or (FullName = ?) or (Password = ?)) ",(search,search,search))
                 res = self.__cur.fetchall()
                 if res: return res
        except sqlite3.Error as e:
            print('Ошибка чтения из БД поиск %s' % (search) + str(e))
            return False
        return True

    def getClass(self):
        sql = '''SELECT * FROM class '''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из бд")
        return []


    def getUsers(self):
        sql = '''SELECT * FROM Users '''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из бд")
        return []


    def getMenu(self):
        sql = '''SELECT * FROM Users'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
             print("Ошибка чтения из БД")
        return []

#Для регистрации
    def addUser(self,FullName, Login, Password, Admin=None):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM Users WHERE '{Login}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким логином уже существует")
                return False

            self.__cur.execute("INSERT INTO Users VALUES(NULL, ?, ?, ?, ?)", (FullName, Login, Password, Admin))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя"+str(e))
            return False

        return True


#Добавление уроков


    def Addf(self, timestart, timestop, teacher,t,y=None,u=None):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM Offices WHERE '{teacher}'")
            res = self.__cur.fetchone()


            self.__cur.execute("INSERT INTO Offices VALUES(NULL, ?, ?, ?, ?, ?, ?)", (timestart, timestop, t,teacher,y,u))
            self.__db.commit()
            print("uspex")
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя" + str(e))
            return False

        return True

    def getOffice(self,classname):

        try:
            self.__cur.execute(f"SELECT * FROM Offices WHERE (officename = ?) ORDER BY startlesson ASC",(classname,))
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка чтения из бд" + str(e))
        return []

    def delof(self, startlesson, endlesson, lessonname):

        try:
                self.__cur.execute(f"DELETE FROM Offices where (lessonname = ?) and (startlesson = ?) and (endlesson = ?)", (lessonname,startlesson,endlesson))
                self.__db.commit()
                print('Запись %s спешно удалена' % (lessonname))

        except sqlite3.Error as e:
            print("Ошибка" + str(e))
            return False
        return True


#для авторизации
    def getUser(self, id_user):
        try:
            self.__cur.execute(f"SELECT * FROM Users WHERE id_user ={id_user} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не авторизован")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД getUser"+str(e))

        return False

#для авторизации
    def getUserByLogin(self, Login,Password):
        try:
            self.__cur.execute(f"SELECT * FROM Users WHERE (Login = '{Login}') and (Password='{Password}')  LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не залогинен")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД Login" + str(e))

        return False

def getUserByReg(self,id_user):
    try:
        self.__cur.execute(f"SELECT FullName, Login, Password FROM Users WHERE id ={id_user} LIMIT 1")
        res = self.__cur.fetchone()
        if res:
            return res
    except sqlite3.Error as e:
        print("Ошибка получения пользователя из БД Reg" + str(e))

    return False


def getUsersAnonce(self):
    try:
        self.__cur.execute(f"SELECT id, Fullname, Login, Password FROM Users ORDER BY time DESC")
        res = self.__cur.fetchall()
        if res: return res
    except sqlite3.Error as e:
        print("Ошибка получения пользователя из БД Anonce"+str(e))

    return[]







def calendar_events(self):
    try:
        self.__cur.execute("SELECT id, title, url, class, UNIX_TIMESTAMP(start_date)*1000 as start, UNIX_TIMESTAMP(end_date)*1000 as end FROM event")
        rows = self.__cur.fetchall()
        resp = jsonify({'success' : 1, 'result' : rows})
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)