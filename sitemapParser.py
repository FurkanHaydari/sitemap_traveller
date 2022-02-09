import database.mysql_create_database
import database.mysql_create_tables
import database.mysql_insert as seed 
from database.exampleSitemaps import Sitemaps     #Örnek Sitemaplerin olduğu liste
import models.index as index
import models.db as db
from urllib.parse import urlparse   #url parse etmek için


#<----------Eğer Yoksa Tablo Oluştur------------->

def parseUrl(url):
    parsedUrl=urlparse(url)     
    domain=parsedUrl.netloc
    a=url.split('/')[-1]
    kategori=a.split('.')[0]
    return domain,kategori
#<----------------------------------------------->


#<----------urlSets linklerini, ilgili tabloya kaydetme fonksiyonu------------->
def seedUrlSetLinks(url,lastmod):                                                           
    domain,kategori=parseUrl(url)
    seed.degerEkleUrlSets(domain,url,kategori,lastmod)
#<----------------------------------------------------------------------------->


#<----------XML Döküman Parçalayıcı------------->
def parser(lxmlElement):
    loc=lxmlElement.xpath('.//*[local-name()="loc"]')
    lastmod=lxmlElement.xpath('.//*[local-name()="lastmod"]')
    url=loc[0].text
    domain,kategori=parseUrl(url)

    xml = index.sendRequest(url)
                                                             
    if xml == None:
        print("Undefined Döküman: ", url)
        seed.degerEkleSitemapIndex(domain,url,kategori,'',-2)    
    else:
        if xml is not False:                                                             #Request başarıyla atıldıysa eğer
            sitemapType = index.getSitemapType(xml)                                          #dökümanın tipini öğren
            if(sitemapType == 'urlset'): 
                if(lastmod):
                    seed.degerEkleUrlSets(domain,url,kategori,lastmod[0].text)
                else:
                    seed.degerEkleUrlSets(domain,url,kategori,'')
            elif(sitemapType == 'sitemapindex'): 
                if(lastmod):
                    seed.degerEkleSitemapIndex(domain,url,kategori,lastmod[0].text,0)
                else:
                    seed.degerEkleSitemapIndex(domain,url,kategori,'',0)
            else:
                print("Undefined Döküman: ", url)
                seed.degerEkleSitemapIndex(domain,url,kategori,'',-2)                      #-2 status undefined doc
        else:
                print("404 Not Found ", url)
                seed.degerEkleSitemapIndex(domain,url,kategori,'',-1)                      #-1 status can not reach doc
#<----------------------------------------------------->        





#<---------------------Sitemapindex tipindeki linki tabloya kaydet ve dökümanı parçala-------------------------------->  
def seedSitemapindexLinks(xml,link,lastmod):          

    domain,kategori=parseUrl(link)
    seed.degerEkleSitemapIndex(domain,link,kategori,lastmod,1)
    sitemapList=xml.xpath('//*[local-name()="sitemap"]')
   
    for i in range(len(sitemapList)):
        parser(sitemapList[i])
#<------------------------------------------------------------------------------------------------------------------->  






#<---------------------------------Main------------------------------------->
def main(url):                                                             #Sitemap linkini bu fonksiyona atın. 
    print('Sitemap Parsing... ', url)
    xml = index.sendRequest(url)
    domain,kategori=parseUrl(url)
    
    if xml == None:
        print("Undefined Döküman: ", url)
        seed.degerEkleSitemapIndex(domain,url,kategori,'',-2)
    else:    
        if xml is not False:                                               #Robots.txt izin veriyors eğer
            sitemapType = index.getSitemapType(xml)                         #dökümanın tipini öğren
            if(sitemapType == 'urlset'):            
                seedUrlSetLinks(url,lastmod='')                            #urlSet işlemlerini çalıştır
            elif(sitemapType == 'sitemapindex'):
                seedSitemapindexLinks(xml,url,lastmod='')                  #sitemap index işlemlerini çalıştır  
            else:
                print("Undefined Döküman: ", url)
                seed.degerEkleSitemapIndex(domain,url,kategori,'',-2)
        else:
                print("404 Not Found ", url)                
                seed.degerEkleSitemapIndex(domain,url,kategori,'',-1)
    print('Successfuly Finished')
#<-------------------------------------------------------------------------------->



#<------------------------------- Tabloda isActif=0 olan linkleri sorgulama ve parse etme fonksiyonları----------------------->






def sitemapTableparser(link): 

    xml = index.sendRequest(link)                               #Fonksiyona gelen linkin dökümanını elde et

                                        
#Request başarıyla atıldıysa eğer 
    if xml is not False:                                               
        if xml is not None:
            db.sitemapindexStatusBirYap(link)                             #Gelen linki database'de isAktif=1 yap
            sitemapList=xml.xpath('//*[local-name()="sitemap"]')        #sitemap listesini xpath ile çek
            urlList=xml.xpath('//*[local-name()="url"]')
            if sitemapList is not None:
                for i in sitemapList:
                    parser(i)  
            if urlList is not None:                                             #bütün sitemapleri parser'a gönder
                for i in urlList:
                    parser(i) 
        else:
            print("undefined Döküman",link)
    else:
        print("404 Not Found From Sitemap index: ", link)






def statusSifirCrawlerFromDatabase():                      #Sitemap index tablosundaki isAktif=0 olan tüm linkleri çek ve bunları parser fonksiyonuna yolla.
    data=db.findAllStatusSıfır()                          #isAktif=0 olan bütün datayı çek
    if data is not None:
        for i in data:
            sitemapTableparser(i[0])                        #data değişkeninin yapısı liste içinde liste,her döngüde i[0][0] saf linki vericek

def statusEksiBirCrawlerFromDatabase():                      #Sitemap index tablosundaki isAktif=0 olan tüm linkleri çek ve bunları parser fonksiyonuna yolla.
    data=db.findAllStatusEksiBir()                          #isAktif=0 olan bütün datayı çek
    if data is not None:
        for i in data:
            sitemapTableparser(i[0])                        #data değişkeninin yapısı liste içinde liste,her döngüde i[0][0] saf linki vericek

def statusEksiIkiCrawlerFromDatabase():                      #Sitemap index tablosundaki isAktif=0 olan tüm linkleri çek ve bunları parser fonksiyonuna yolla.
    data=db.findAllStatusEksiIki()                          #isAktif=0 olan bütün datayı çek
    if data is not None:
        for i in data:
            sitemapTableparser(i[0])                        #data değişkeninin yapısı liste içinde liste,her döngüde i[0][0] saf linki vericek




def checkStatusSifir():
    bayrak=db.sitemapindexStatusSıfırKalmısMı()           #Sitemapindex tablosunda isActif=0 varsa bayrak=true, yoksa false.
    while bayrak:                                           #Bayrak=True iken
        print('Sitemap içindeki sitemapler ayrıştırılıyor...')
        statusSifirCrawlerFromDatabase()                   #Databasedeki isActif=0 olan linkleri parser'a sokan fonksiyon.
        bayrak=db.sitemapindexStatusSıfırKalmısMı()       #Sitemapindex tablosunda isActif=0 varsa bayrak=true, yoksa false

def checkStatusEksiBir():
    bayrak=db.sitemapindexStatusEksiBirKalmısMı()           #Sitemapindex tablosunda isActif=0 varsa bayrak=true, yoksa false.
    if bayrak is not None:                                           #Bayrak=True iken
        print('404 not found olan sitemapler tekrar deneniyor...')
        statusEksiBirCrawlerFromDatabase()                   #Databasedeki status=-1 olan linkleri parser'a sokan fonksiyon.
def checkStatusEksiIki():        
    bayrak=db.sitemapindexStatusEksiIkiKalmısMı()           #Sitemapindex tablosunda isActif=0 varsa bayrak=true, yoksa false.
    if bayrak is not None:                                          #Bayrak=True iken
        print('parçalanamayan sitemapler tekrar deneniyor...')
        statusEksiIkiCrawlerFromDatabase()                   #Databasedeki isActif=0 olan linkleri parser'a sokan fonksiyon.



#<------------------------------- Tanımlamaların Bitişi ------------------------------------->

#<------------------------------- Fonksiyonları Çağırma ------------------------------------->


for i in range (len(Sitemaps)):
    main(Sitemaps[i])                  #Sitemaplerin tutulduğu listeyi yazılıma gönder.

checkStatusSifir()                   #sitemap index Database'inde isActif=0 kalmayana kadar first parseri çalıştır.
checkStatusEksiIki()
checkStatusEksiBir()
print('VERİLER BAŞARIYLA TABLOYA KAYDEDİLDİ.')


#<----------------------------------------- BİTİŞ -------------------------------------------->

