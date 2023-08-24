import mysql.connector
#CREATE USER 'nuevo_usuario' IDENTIFIED BY 'clave123';
class DatabaseConnection:
   _connection = None
@classmethod
def get_connection(cls):
 if cls._connection is None:
    cls._connection = mysql.connector.connect(
       host='127.0.0.1',
        user='nuevo_usuario',
        port = "3306",
        password='clave123',
        database='sales',
    )
 return cls._connection
@classmethod
def execute_query(cls, query, params=None):
    cursor = cls.get_connection().cursor()
    cursor.execute(query, params)
    cls._connection.commit
    return cursor
@classmethod
def fetch_one(cls, query, params=None):
    cursor = cls.get_connection().cursor()
    cursor.execute(query, params)
    return cursor.fetchone()
@classmethod
def fetch_all(cls, query, params=None):
 cursor = cls.get_connection().cursor()
 cursor.execute(query, params)
 return cursor.fetchall()
@classmethod
def close_connection(cls):
 if cls._connection is not None:
   cls._connection.close()
   cls._connection = None