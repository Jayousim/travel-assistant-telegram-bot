import mysql.connector


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


@Singleton
class DBConnection(object):

    def __init__(self):
        self.my_db = None
        try:
            self.my_db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="sql_intro"
            )
        except:
            print("error connecting to data base")

    def get_db(self):
        return self.my_db


def get_previous_message(chat_id):
    my_cursor = DBConnection.Instance().get_db().cursor()
    my_cursor.execute(f"SELECT previous_message FROM Users where chat_id = {chat_id}")
    my_result = my_cursor.fetchall()
    return my_result


def insert_new_message(chat_id, message):
    my_db = DBConnection.Instance().get_db()
    my_cursor = my_db.cursor()

    sql = "INSERT INTO Users (chat_id, previous_message) VALUES (%s, %s)"
    val = (chat_id, message)
    my_cursor.execute(sql, val)

    my_db.commit()
    print(my_cursor.rowcount, "record inserted.")
    return

#insert_new_message(12, "cool")
get_previous_message(12)