#import mysql.connector
import pymysql


class Singleton:

    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)


destinations = "(chat_id INTEGER," \
               "destination VARCHAR(64)," \
               "category VARCHAR(64)," \
               "hotel_name VARCHAR(64)," \
               "activity_name VARCHAR(64)," \
               "activity_url VARCHAR(500)," \
               "PRIMARY KEY(chat_id,destination,category,hotel_name,activity_name, activity_url))"


@Singleton
class DBConnection(object):

    def __init__(self):
        self.my_db = None
        try:
            #self.my_db = mysql.connector.connect(
            self.my_db = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="",
                #auth_plugin='mysql_native_password'
            )
            self.create_tables()
        except:
            print("error connecting to data base")

    def get_db(self):
        return self.my_db

    def create_tables(self):
        with self.my_db.cursor() as cursor:
            print("create table begin")
            query = f"DROP TABLE IF EXISTS destinations"
            cursor.execute(query)
            self.my_db.commit()
            query = f"CREATE TABLE IF NOT EXISTS destinations {destinations}"
            cursor.execute(query)
            self.my_db.commit()
            print("create table end")



#mycursor = DBConnection.Instance().get_db().cursor()
#mycursor.execute("drop TABLE Users")
#mycursor.execute("CREATE TABLE Users (chat_id int not null primary key,status smallint not null, message varchar(50))")


def get_status(chat_id):
    my_db = DBConnection.Instance().get_db()
    cur = my_db.cursor()
    cur.execute(f"SELECT status FROM Users where chat_id = {chat_id}")
    my_result = cur.fetchall()
    return my_result


def get_message(chat_id):
    my_db = DBConnection.Instance().get_db()
    cur = my_db.cursor()
    cur.execute(f"SELECT message FROM Users where chat_id = {chat_id}")
    my_result = cur.fetchall()
    return my_result


def insert_new_message(chat_id, status, mess):
    my_db = DBConnection.Instance().get_db()
    my_cursor = my_db.cursor()
    message = get_status(chat_id)
    if len(message) == 0:
        sql = "INSERT INTO Users (chat_id, status, message) VALUES (%s, %s, %s)"
        val = (chat_id, status, mess)
        my_cursor.execute(sql, val)

        my_db.commit()
        print(my_cursor.rowcount, "record inserted.")
        return "success"
    else:
        sql = "UPDATE Users SET status = %s, message = %s WHERE chat_id = %s"
        val = (status, mess, chat_id)
        my_cursor.execute(sql, val)
        my_db.commit()
        print(my_cursor.rowcount, "record(s) affected")
        return "success"

