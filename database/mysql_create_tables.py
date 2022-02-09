import mysql.connector
from mysql.connector import errorcode


mydb = mysql.connector.connect(
host="localhost",
user="root",
#password="yourpassword",
database="SITEMAPS"
)

mycursor = mydb.cursor()
DB_NAME = 'SITEMAPS'

TABLES = {}
TABLES['sitemapindex'] = (
    "CREATE TABLE `sitemapindex` ("
    "  `ID` int(11) NOT NULL AUTO_INCREMENT,"
    "  `domain` varchar(250) NOT NULL,"
    "  `url` varchar(1000) UNIQUE,"
    "  `kategori` varchar(40) NOT NULL,"
    "  `lastmod` varchar(40) NOT NULL,"
    "  `Status` tinyint NOT NULL DEFAULT 0,"
    "  PRIMARY KEY (`ID`)"
    ") ENGINE=InnoDB AUTO_INCREMENT=0")

TABLES['urlSets'] = (
    "CREATE TABLE `urlSets` ("
    "  `ID` int(11) NOT NULL AUTO_INCREMENT,"
    "  `domain` varchar(250) NOT NULL,"
    "  `url` varchar(1000) UNIQUE,"
    "  `kategori` varchar(40),"
    "  `lastmod` varchar(40),"
    "  `Status` tinyint NOT NULL DEFAULT 0,"
    "  PRIMARY KEY (`ID`)"
    ") ENGINE=InnoDB AUTO_INCREMENT=0")

cnx = mysql.connector.connect(user='root')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    # if err.errno == errorcode.ER_BAD_DB_ERROR:
    #     create_database(cursor)
    #     print("Database {} created successfully.".format(DB_NAME))
    #     cnx.database = DB_NAME
    # else:
    #     print(err)
    #     exit(1)

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

# cursor.close()
# cnx.close()
# sql = "INSERT INTO sitemapindex (domain, url) VALUES (%s, %s)"
# val = ("John", "Highway 21")
# mycursor.execute(sql, val)

# mydb.commit()

# print(mycursor.rowcount, "record inserted.")