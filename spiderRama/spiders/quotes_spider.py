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
    
    name = "quotes"
    
    def start_requests(self):
        urls = [
            'https://www.ramajudicial.gov.co/web/juzgado-015-laboral-de-barranquilla/64',
            # 'https://www.ramajudicial.gov.co/web/secretaria-tribunal-administrativo-del-atlantico/287',
            # 'https://www.ramajudicial.gov.co/web/juzgado-015-civil-del-circuito-de-barranquilla/105',
        ]
        for url in urls:
            yield scrapy.Request(url=get_scrapeops_url(url), callback=self.parse)

    def parse(self, response):
        
        #Buscar enlaces del mes actual
        buscarEnlacesMesActual = False
        #Dominio:
        dominioRama = 'https://www.ramajudicial.gov.co'
        #Nombre del archivo:
        filename = f'scraping_tablas_enlaces_extraidos_{buscarEnlacesMesActual}.html'
        
        with open(filename, 'w') as f:
            tablasEnlacesList = [contenedorTable.css('table').getall() for contenedorTable in response.xpath('//div[contains(@class, "aui-tabview-content-item")]')]
            # for table in tableList:
            #     tablasEnlacesList =
            # print(tablas) #0.6 0.3 0.3 0.3 = 1.5 
            # f.write(str(tablas)+'\n')
            # exit()
                        
            if buscarEnlacesMesActual:    
                tablasEnlacesList = ""   
                mes = int(format(datetime.datetime.now().strftime('%m')))
                n=0
                for scope in response.xpath('//div[contains(@class, "aui-tabview-content-item")]'): 
                    n=n+1
                    if (n==mes):
                        tablasEnlacesList = scope.css('table').getall()
            
            # print( tablasEnlacesList )
            # exit()
            if len(tablasEnlacesList)>0:
                #Se descarta enlaces exactamente iguales:
                # tablasEnlacesListSinDuplicados = set(tablasEnlacesList)
                
                for tablaEnlace in tablasEnlacesList: 
                    if type(tablaEnlace)==list:
                        for tb in tablaEnlace:
                            # if( re.search("^"+dominioRama+"*", tb) ):
                            #     print("Tiene el dominio")
                            # else:
                            #     tb = dominioRama + str(tb.css('a').getall())
                                
                            # f.write(str(tb)+'\n')
                            # print(tb.replace("\x00", ""))
                            f.write(str(tb).replace(["\x00"], "")+'\n')
                            
                    else:
                        print("No es list ------------>",  type(tablaEnlace))
                             
                    
                    
            self.log(f'Saved file {filename}')
            
            