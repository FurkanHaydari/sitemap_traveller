import requests   
from lxml import etree              #xml parçalama kütüphanesi


#Request atma fonksiyonu
def sendRequest(url):
    try:
        r = requests.get(url)        

        try:
            
            xml = etree.fromstring(r.content)
                
        except:

            xml= None

    except:

        xml=False

    finally:
        return xml



#sayfanın tipi url set mi yok sitemap index mi kontrol fonksiyonu
def getSitemapType(xml):

    sitemapindex = xml.xpath('//*[local-name()="sitemapindex"]')
    sitemap = xml.xpath('//*[local-name()="urlset"]')

    if sitemapindex:
        return 'sitemapindex'
    elif sitemap:
        return 'urlset'
    else:
        return 'none'



