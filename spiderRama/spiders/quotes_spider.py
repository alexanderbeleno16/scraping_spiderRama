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
        buscarEnlacesMesActual = True
        #Dominio:
        dominioRama = 'https://www.ramajudicial.gov.co'
        #Nombre del archivo:
        filename = f'scraping_enlaces_extraidos_{buscarEnlacesMesActual}.txt'
        
        with open(filename, 'w') as f:
            enlacesList = response.xpath('//a[contains(@href, "documents/")]/@href').getall()
                        
            if buscarEnlacesMesActual:    
                enlacesList = ""   
                mes = int(format(datetime.datetime.now().strftime('%m')))
                n=0
                for scope in response.xpath('//div[contains(@class, "aui-tabview-content-item")]'): 
                    n=n+1
                    if (n==mes):
                        enlacesList = scope.css('a').xpath('@href').getall()
            
            if len(enlacesList)>0:
                #Se descarta enlaces exactamente iguales:
                enlacesListSinDuplicados = set(enlacesList)
                
                for enlacesRama in enlacesListSinDuplicados:                    
                    if( re.search("^"+dominioRama+"*", enlacesRama) ):
                        print("Tiene el dominio")
                    else:
                        enlacesRama = dominioRama + str(enlacesRama)
                        
                    f.write(str(enlacesRama)+'\n')
                    
            self.log(f'Saved file {filename}')
            
            