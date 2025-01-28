import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='mysql',
            user='root',       
            password='rootpassword',  
            database='visitor_management' 
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error while connecting to the database: {e}")
        return None
