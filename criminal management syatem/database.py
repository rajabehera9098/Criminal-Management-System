import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        username='root',
        password='Root@1234',
        database='management'
    )