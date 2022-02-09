# import sqlite3
# con = sqlite3.connect("sitemap.db")
import mysql.connector
from mysql.connector import errorcode




mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  #password="yourpassword",
  database="SITEMAPS"
)
cursor=mydb.cursor()


def findAllStatusSıfır():
    cursor.execute("SELECT url FROM sitemapindex WHERE Status=0")
    data=cursor.fetchall()    
    return data

def findAllStatusEksiBir():
    cursor.execute("SELECT url FROM sitemapindex WHERE Status=-1")
    data=cursor.fetchall()    
    return data

def findAllStatusEksiIki():
    cursor.execute("SELECT url FROM sitemapindex WHERE Status=-2")
    data=cursor.fetchall()    
    return data

def sitemapindexStatusBirYap(link):
    cursor.execute("UPDATE sitemapindex SET Status=1 WHERE url=%s",([link]))
    mydb.commit()

def sitemapindexStatusSıfırKalmısMı():
    cursor.execute("SELECT url FROM sitemapindex WHERE Status=0 LIMIT 1")
    data=cursor.fetchall()    
    return data

def sitemapindexStatusEksiBirKalmısMı():
    cursor.execute("SELECT url FROM sitemapindex WHERE Status=-1 LIMIT 1")
    data=cursor.fetchall()    
    return data

def sitemapindexStatusEksiIkiKalmısMı():
    cursor.execute("SELECT url FROM sitemapindex WHERE Status=-2 LIMIT 1")
    data=cursor.fetchall()    
    return data

def degerOkuUrlSets():
    cursor.execute("SELECT url FROM urlSets WHERE Status=0")
    data=cursor.fetchall()    
    return data

def urlSetsStatusSıfırKalmısMı():
    cursor.execute("SELECT url FROM urlSets WHERE Status=0 LIMIT 1")
    data=cursor.fetchall()    
    return data

def urlSetsStatusBirYap(link):
    cursor.execute("UPDATE urlSets SET Status=1 WHERE url=%s",([link]))
    mydb.commit()