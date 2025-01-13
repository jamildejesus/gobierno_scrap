import scrapy
import logging
import requests
from datetime import date
from scrapy.exceptions import CloseSpider
from gobierno_scrap.utils.methods import UtilsMethods
from scrapy.selector import Selector
from datetime import datetime
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from gobierno_scrap.items import CampecheIniciativasItem

class CampecheIniciativasSpider(scrapy.Spider):
    name = "CampecheIniciativas"
    allowed_domains = ["www.congresocam.gob.mx"]
    start_urls = ["https://www.congresocam.gob.mx/iniciativas/"]

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'redirect': 'follow'}

    def parse(self, response):
        currentDate = self.getCurrentDate()
        #currentDate = '27/01/2024'

# ----------------------------------------------------------------------------------  
        lxivlegislatura = response.xpath('//div[@id="tab-3423dc81019662a3dd1"]')
        directoryListeriv = lxivlegislatura.css('div.directory-lister-wrapper div a')
        urlAttachAux = []
        for dl in directoryListeriv:
          href = dl.attrib['href']
          #urlAttachAux.append(href)
          title = response.css('h1.entry-title::text').get() + ' ' + response.xpath('//a[@id="fusion-tab-lxvlegislatura"]/h4/text()').get()
          dateRaw = self.cleanText(currentDate)
          date = dateRaw
          item = CampecheIniciativasItem()
          item['title'] = href
          item['urlPage'] = response.url
          item['sinopsys'] = 'N/A'
          item['federalEstatal'] = "Congreso"
          item['state'] = "Campeche"
          item.parse_date_str(date)
          urlAttach = self.createUrlAttachField(href)
          item['urlAttach'] = urlAttach
          item['collectionName'] = self.name
          yield item

# ----------------------------------------------------------------------------------  
        lxivlegislatura = response.xpath('//div[@id="tab-961485a9767db92a99b"]')
        directoryListeriv = lxivlegislatura.css('div.directory-lister-wrapper div a')
        urlAttachAux = []
        for dl in directoryListeriv:
          href = dl.attrib['href']
          #urlAttachAux.append(href)
          title = response.css('h1.entry-title::text').get() + ' ' + response.xpath('//a[@id="fusion-tab-lxivlegislatura"]/h4/text()').get()
          dateRaw = self.cleanText(currentDate)
          date = dateRaw
          item = CampecheIniciativasItem()
          item['title'] = href
          item['urlPage'] = response.url
          item['sinopsys'] = 'N/A'
          item['federalEstatal'] = "Congreso"
          item['state'] = "Campeche"
          item.parse_date_str(date)
          urlAttach = self.createUrlAttachField(href)
          item['urlAttach'] = urlAttach
          item['collectionName'] = self.name
          yield item

# ----------------------------------------------------------------------------------          
        lxiiilegislatura = response.xpath('//div[@id="tab-3cddf76019624b8b77b]')
        directoryListeriii = lxiiilegislatura.css('div.directory-lister-wrapper div a')
        urlAttachAux = []
        for dl in directoryListeriii:
          href = dl.attrib['href']
          #urlAttachAux.append(href)
          title = response.css('h1.entry-title::text').get() + ' ' + response.xpath('//a[@id="fusion-tab-lxiiilegislatura"]/h4/text()').get()
          dateRaw = self.cleanText(currentDate)
          date = dateRaw
          item = CampecheIniciativasItem()
          item['title'] = title
          item['urlPage'] = response.url
          item['sinopsys'] = 'N/A'
          item['federalEstatal'] = "Congreso"
          item['state'] = "Campeche"
          item.parse_date_str(date)
          urlAttach = self.createUrlAttachField(href)
          item['urlAttach'] = urlAttach
          item['collectionName'] = self.name
          print("Guardado")
        yield item

# ----------------------------------------------------------------------------------  
        lxiilegislatura = response.xpath('//div[@id="tab-5c2e614c8c82162332d"]')
        directoryListerii = lxiilegislatura.css('div.directory-lister-wrapper div a')
        urlAttachAux = []
        for dl in directoryListerii:
          href = dl.attrib['href']
          #urlAttachAux.append(href)
          title = response.css('h1.entry-title::text').get() + ' ' + response.xpath('//a[@id="fusion-tab-lxiilegislatura"]/h4/text()').get()
          dateRaw = self.cleanText(currentDate)
          date = dateRaw
          item = CampecheIniciativasItem()
          item['title'] = href
          item['urlPage'] = response.url
          item['sinopsys'] = 'N/A'
          item['federalEstatal'] = "Congreso"
          item['state'] = "Campeche"
          item.parse_date_str(date)
          urlAttach = self.createUrlAttachField(href)
          item['urlAttach'] = urlAttach
          item['collectionName'] = self.name
          yield item

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
        """
        for ua in urlAttach:
            objAux = []
            objAux = {
                'urlAttach': ua,
                'sinopsys': '',
                'wasParsed': 'procesar'
            }
        """
        objAux = {
                'urlAttach': urlAttach,
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

