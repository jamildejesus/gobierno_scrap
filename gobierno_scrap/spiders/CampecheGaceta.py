import scrapy
import logging
import requests
from datetime import date
from scrapy.exceptions import CloseSpider
from gobierno_scrap.utils.methods import UtilsMethods
from gobierno_scrap.items import CampecheGacetaItem
from scrapy.selector import Selector
from datetime import datetime
from time import sleep

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

class CampecheGacetaSpider(scrapy.Spider):
    name = "CampecheGaceta"
    allowed_domains = ["www.congresocam.gob.mx"]
    start_urls = ["https://www.congresocam.gob.mx/gaceta"]

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'redirect': 'follow'}

    def parse(self, response):
        #currentDate = self.getCurrentDate()
        currentDate = '26/11/2024'  
        periodoActual = response.xpath('//div[@id="tab-de758e0b3e0d0cc1f1c"]')
        directoryListeriv = periodoActual.css('div.directory-lister-wrapper div a')
        urlAttachAux = []
        for dl in directoryListeriv:
            href = dl.attrib['href']
            sacarFecha = str(href).split('_')
            fecha = str(sacarFecha[len(sacarFecha)-1]).split('.')[0]
            lonf = len(fecha)
            loni = len(fecha)-4
            strAno = str(fecha[loni:lonf])
            #if len(fecha[2:loni]) == 2: strMes = str(fecha[2:loni])
            #if len(fecha[2:loni]) > 2: strMes = self.getMes(fecha[2:loni])
            strMes=fecha[2:len(fecha)-4]
            strMes= self.getMes(strMes)
            fecha = f'{fecha[0:2]}/{strMes}/{strAno}'

            if currentDate == fecha:
                urlAttachAux.append(href)

        title = response.css('h1.entry-title::text').get() + ' ' + response.xpath('//a[@id="fusion-tab-periodoactual"]/h4/text()').get()
        dateRaw = self.cleanText(currentDate)
        date = dateRaw

        item = CampecheGacetaItem()
        item['title'] = title
        item['urlPage'] = response.url
        item['sinopsys'] = 'N/A'
        item['federalEstatal'] = "Congreso"
        item['state'] = "Campeche"
        item.parse_date_str(date)
        urlAttach = self.createUrlAttachField(urlAttachAux)
        item['urlAttach'] = urlAttach
        item['collectionName'] = self.name

        yield item

# ----------------------------------------------------------------------------------          
        # lxivlegislatura = response.xpath('//div[@id="tab-0f652ae3b32c0459383"]')
        # directoryListeriv = lxivlegislatura.css('div.directory-lister-wrapper div a')
        # urlAttachAux = []
        # for dl in directoryListeriv:
        #   href = dl.attrib['href']
        #   urlAttachAux.append(href)

        # title = response.css('h1.entry-title::text').get() + ' ' + response.xpath('//a[@id="fusion-tab-lxivlegislatura"]/h4/text()').get()
        # dateRaw = self.cleanText(currentDate)
        # date = dateRaw

        # item = CampecheGacetaItem()
        # item['title'] = title
        # item['urlPage'] = response.url
        # item['sinopsys'] = 'N/A'
        # item['federalEstatal'] = "Gaceta"
        # item['state'] = "Campeche"
        # item.set_date_iso(date)
        # urlAttach = self.createUrlAttachField(urlAttachAux)
        # item['urlAttach'] = urlAttach
        # item['collectionName'] = self.name

        # yield item

# ----------------------------------------------------------------------------------  
        # lxiiilegislatura = response.xpath('//div[@id="tab-6b5665f47f4e0f9fe63"]')
        # directoryListeriii = lxiiilegislatura.css('div.directory-lister-wrapper div a')
        # urlAttachAux = []
        # for dl in directoryListeriii:
        #   href = dl.attrib['href']
        #   urlAttachAux.append(href)

        # title = response.css('h1.entry-title::text').get() + ' ' + response.xpath('//a[@id="fusion-tab-lxiiilegislatura"]/h4/text()').get()
        # dateRaw = self.cleanText(currentDate)
        # date = dateRaw

        # item = CampecheGacetaItem()
        # item['title'] = title
        # item['urlPage'] = response.url
        # item['sinopsys'] = 'N/A'
        # item['federalEstatal'] = "Gaceta"
        # item['state'] = "Campeche"
        # item.set_date_iso(date)
        # urlAttach = self.createUrlAttachField(urlAttachAux)
        # item['urlAttach'] = urlAttach
        # item['collectionName'] = self.name

        # yield item

# ----------------------------------------------------------------------------------  
        # lxiilegislatura = response.xpath('//div[@id="tab-b4d120aac1c6755010c"]')
        # directoryListerii = lxiilegislatura.css('div.directory-lister-wrapper div a')
        # urlAttachAux = []
        # for dl in directoryListerii:
        #   href = dl.attrib['href']
        #   urlAttachAux.append(href)

        # title = response.css('h1.entry-title::text').get() + ' ' + response.xpath('//a[@id="fusion-tab-lxiilegislatura"]/h4/text()').get()
        # dateRaw = self.cleanText(currentDate)
        # date = dateRaw

        # item = CampecheGacetaItem()
        # item['title'] = title
        # item['urlPage'] = response.url
        # item['sinopsys'] = 'N/A'
        # item['federalEstatal'] = "Gaceta"
        # item['state'] = "Campeche"
        # item.set_date_iso(date)
        # urlAttach = self.createUrlAttachField(urlAttachAux)
        # item['urlAttach'] = urlAttach
        # item['collectionName'] = self.name

        # yield item

    def finalCleanText(self, text):
        if UtilsMethods.checkIfTextIsEmpty(text) == '-':
            return 'na'

        textClean = UtilsMethods.stripAccents(text)
        textEllipsis = UtilsMethods.removeEllipsis(textClean)
        return UtilsMethods.upperCaseText(textEllipsis)

    def cleanText(self, text):
        firstText = UtilsMethods.removeNonBreakingSpace(text)
        return UtilsMethods.removeNewBlankSpace(firstText)

    def createUrlAttachField(self, urlAttach):
        urlAttachArrayList = []
        if urlAttach == None or len(urlAttach) == 0:
            urlAttach = 'na'
            return urlAttach
        
        for ua in urlAttach:
            objAux = []
            objAux = {
                'urlAttach': ua,
                'sinopsys': '',
                'wasParsed': 'procesar'
            }
            urlAttachArrayList.append(objAux)

        return urlAttachArrayList

    def finalDate(self, dateRaw):
        dateClean = dateRaw.replace(',', '')
        newDate = UtilsMethods.sinaloaComunicacionDateSplit(dateClean)
        return newDate

    def getCurrentDate(self):
        spiderDate = getattr(self, 'SPIDER_DATE', None)  # day/month/year
        if spiderDate:
            formatDate = spiderDate
            print("Desde consola: ", formatDate)
            return formatDate
        else:
            currentDate = date.today()
            formatDate = currentDate.strftime("%d/%m/%Y")
            print("Desde metodo: ", formatDate)
            return formatDate
        
    def getFecha(self, value):
        m = {
            'Enero': "01",
            'Febrero': "02",
            'Marzo': "03",
            'Abril': "04",
            'Mayo': "05",
            'Junio': "06",
            'Julio': "07",
            'Agosto': "08",
            'Septiembre': "09",
            'Octubre': "10",
            'Noviembre': "11",
            'Diciembre': "12"
        }        
        lst = value.split(' ')
        fecha = f"{lst[0].strip()}/{m[lst[2].strip()]}/{lst[3].strip()}"
        return fecha
    
    def getMes(self, value):
        m = {
            'ENERO': "01",
            'FEBRERO': "02",
            'MARZO': "03",
            'ABRIL': "04",
            'MAYO': "05",
            'JUNIO': "06",
            'JULIO': "07",
            'AGOSTO': "08",
            'SEPTIEMBRE': "09",
            'OCTUBRE': "10",
            'NOVIEMBRE': "11",
            'DICIEMBRE': "12"
        }        
        return m[value]
    
