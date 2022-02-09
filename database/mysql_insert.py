import mysql.connector





mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  #password="yourpassword",
  database="SITEMAPS"
)

mycursor=mydb.cursor()
connection = mysql.connector.connect(user='root')
cursor = connection.cursor()

def degerEkleSitemapIndex(domain, url, kategori,lastmod,status):
        try:
                mycursor.execute("insert into sitemapindex (domain, url, kategori,lastmod, status) values (%s, %s, %s, %s,%s)",
                        (domain, url, kategori,lastmod, status))
                mydb.commit()
        except:
                return 


def degerEkleUrlSets(domain, url, kategori, lastmod):
        try:
                mycursor.execute("insert into urlSets (domain, url, kategori,lastmod, status) values (%s, %s, %s, %s,%s)",
                        (domain, url, kategori,lastmod, 0))
                mydb.commit()
        except:
                return
