import mysql.connector
from mysql.connector import Error


mydb = mysql.connector.connect(
host="localhost",
user="root",
#password="yourpassword"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS SITEMAPS")

try:
    connection = mysql.connector.connect(host='localhost',
                                        database='SITEMAPS',
                                        user='root',
                                        
                                        )
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database:", record[0])
        


except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        mycursor.close()
