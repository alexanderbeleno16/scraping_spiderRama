import scrapy

from urllib.parse import urlencode, quote_plus
from scrapy.selector import Selector

import datetime
import re
import random
import sys

API_KEY = '06fa4451-9d5e-474e-acee-576cf7bccf1e'  

def get_scrapeops_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload) #urlencode(payload)
    return proxy_url


class QuotesSpider(scrapy.Spider):
    
    #____________________________________________________________________________________
    #___________________________________Prueba #2________________________________________
    #____________________________________________________________________________________
    name = "quotes"
    
    def start_requests(self):
        urls = [
            # 'http://quotes.toscrape.com/page/2/',
            # 'https://www.ramajudicial.gov.co/web/juzgado-015-laboral-de-barranquilla/64',
            # 'https://www.ramajudicial.gov.co/web/secretaria-tribunal-administrativo-del-atlantico/287',
            'https://www.ramajudicial.gov.co/web/juzgado-015-civil-del-circuito-de-barranquilla/105',
        ]
        for url in urls:
            yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse)

    def parse(self, response):
        
        #Buscar enlaces del mes actual
        buscarEnlacesMesActual = True
        
        #Dominio:
        dominioRama = 'https://www.ramajudicial.gov.co'
        
        #Nombre del archivo:
        filename = f'scraping_enlaces_extraidos_{buscarEnlacesMesActual}.txt'
        
        with open(filename, 'w') as f:
            #Imprime todo el html de la URL:
            # print(response.body)
            
            #Imprime todos los enlaces que existan en el html de la URL:
            # print(response.css('a').xpath('@href').getall())
            
            #Imprime todos los enlaces de documentos que existan en el html de la URL:
            # print(response.xpath('//a[contains(@href, "documents/")]/@href').getall())
            
            enlacesList = response.xpath('//a[contains(@href, "documents/")]/@href').getall()
            
            
            
            
            # print("CONTENEDOR TABS MESEs ------->" , response.xpath('//div[contains(@class, "aui-tabview-content-item")]').getall() )
            # print("CONTENEDOR TABS MESEs ------->" , response.xpath('//div[contains(@class, "aui-tabview-content-item")]').getall())
            # exit()
            
            
            
            
            if buscarEnlacesMesActual:    
                enlacesList = ""   
                mes = int(format(datetime.datetime.now().strftime('%m')))
                #Se recorre las 
                
                # print(response.xpath('//div[contains(@class, "aui-tabview-content-item")]').getall())
                n=0
                for scope in response.xpath('//div[contains(@class, "aui-tabview-content-item")]'): 
                # for scope in response.css('div > table').getall(): 
                    # print(scope)
                    n=n+1
                    if (n==mes):
                        # print(scope.css('a').xpath('@href').getall())
                        # print("encontrado:", scope.css('a').xpath('@href').getall()) 
                        enlacesList = scope.css('a').xpath('@href').getall()
                    
                        # print("DEL MES ------------>" , scope.css('a').xpath('@href').getall())
                        # print("DEL MES ------------>" , scope.css('a').xpath('@href').getall())
            
            # exit()
            #Imprime cantidad enlaces:
            # print("Cantidad enlaces encontrado ---->",len(enlacesList))
            
            if len(enlacesList)>0:
                #Se descarta enlaces exactamente iguales:
                enlacesListSinDuplicados = set(enlacesList)
                
                for enlacesRama in enlacesListSinDuplicados:                    
                    # print( "EL ENLACE CONTIENE EL DOMINIO -->", re.search("^"+dominioRama+"*", enlacesRama) )
                    if( re.search("^"+dominioRama+"*", enlacesRama) ):
                        print("Tiene el dominio")
                    else:
                        enlacesRama = dominioRama + str(enlacesRama)
                        
                    f.write(str(enlacesRama)+'\n')
            
            # f.write(response.body)
            self.log(f'Saved file {filename}')
            
            