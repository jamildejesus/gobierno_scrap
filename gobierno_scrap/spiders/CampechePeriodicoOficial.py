import scrapy
import logging
from datetime import datetime
from scrapy.exceptions import CloseSpider
from gobierno_scrap.items import CampechePeriodicoOficialItem
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

class CampechePeriodicoOficialSpider(scrapy.Spider):
    name = "CampechePeriodicoOficial"
    allowed_domains = ["periodicooficial.campeche.gob.mx"]
    start_urls = ["http://periodicooficial.campeche.gob.mx/sipoec/public/documentos"]

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'redirect': 'follow'}

    def parse(self, response): 
        currentDate = self.getCurrentDate()
        currentDate = '29/11/2024'
        currDate = datetime.strptime(currentDate, '%d/%m/%Y')
        #currDate = datetime.strptime(currentDate, '%Y/%m/%d')
        strDia = str(currDate.day).zfill(2)
        strMes = str(currDate.month).zfill(2)
        strAno = str(currDate.year).zfill(4)
        currentDateNew = f'{strAno}-{strMes}-{strDia}'

        title = response.css('a.yummy-logo').get()

        documentos = response.css('section.archive-area div div div.single-post')
        if len(documentos) == 0: raise CloseSpider('No hay documentos en la tabla... Hay que revisar el selector') 

        urlAttachAux = []
        for doc in documentos:
            data = doc.css('div.post-author a')
            docPdf = str(data[0].css("a::text").get())
            fechaPdf = str(data[1].css("a::text").get())

            if currentDateNew.strip() == fechaPdf.strip():
                href = f'http://{self.allowed_domains[0]}/sipoec/public/periodicos/{strAno}{strMes}/{docPdf}.pdf'
                urlAttachAux.append(href)

        urlAttach = self.createUrlAttachField(urlAttachAux)
        dateRaw = self.cleanText(currentDate)
        date = dateRaw

        item = CampechePeriodicoOficialItem()
        item['title'] =  "Periódico Oficial del Estado de Campeche" #title
        item['urlPage'] = self.start_urls[0]
        item['sinopsys'] = 'N/A'
        item['federalEstatal'] = 'Estatal'
        item['state'] = 'Campeche'
        item.parse_date_str(date)
        item['urlAttach'] = urlAttach
        item['collectionName'] = self.name

        yield item

    def cleanText(self, text):
        newText = self.removeNewBlankSpace(text)
        return newText

    @staticmethod
    def removeNewBlankSpace(text):
        if text.strip() == '&nbsp':
            return 'na'

        textClean = text.replace('&nbsp;', ' ')
        return textClean
    
    def createUrlAttachField(self, urlAttach):
        urlAttachArrayList = []
        if len(urlAttach) == 0 or urlAttach == None:
            urlAttach = 'na'
            return urlAttach

        objAux = {
            'urlAttach': urlAttach[0],
            'sinopsys': '',
            'wasParsed': 'procesar'
        }
        urlAttachArrayList.append(objAux)
        return urlAttachArrayList

    def getCurrentDate(self):
        spiderDate = getattr(self, 'SPIDER_DATE', None)  # day/month/year
        if spiderDate:
            date = spiderDate
            formatDate = self.changeFormatDate(date)
            logging.info("Desde consola: %s", formatDate)
            return formatDate
        else:
            import datetime
            currentDate = datetime.date.today()
            formatDate = currentDate.strftime("%d/%m/%Y")
            logging.info("Desde metodo: %s", formatDate)
            return formatDate

    def stringSlashDateFormat(self, date):
        year, month, day = date.split('/')
        formatDate = f'{day}/{month}/{year}'
        return formatDate

    def changeFormatDate(self, date):
        day, month, year = date.split('/')
        #formatDate = f'{year}/{month}/{day}'
        formatDate = f'{day}/{month}/{year}'
        return formatDate
    
    def getFecha(self, value):
        months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        lst = value.split(' ')
        dayInt = lst[3].replace(',','').zfill(2)
        monInt = (str(months.index(lst[2].capitalize()) + 1)).zfill(2)
        yearInt = lst[4]
        fecha = "{0}/{1}/{2}".format(yearInt, monInt, dayInt)
        return fecha

