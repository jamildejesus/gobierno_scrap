import scrapy

from datetime import date
from scrapy.exceptions import CloseSpider
from gobierno_scrap.utils.methods import UtilsMethods
from gobierno_scrap.items import TlaxcalaIniciativasItem
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TlaxcalaIniciativasSpider(scrapy.Spider):
    name = "TlaxcalaIniciativas"
    allowed_domains = ["congresodetlaxcala.gob.mx"]
    #start_urls = ["https://congresodetlaxcala.gob.mx/trabajo-legislativos-64/#1674236809672-14d8143a-307d"]
    start_urls = ["https://congresodetlaxcala.gob.mx/iniciativas-2024"]

    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'redirect': 'follow'}


    def parse(self, response):
        rows = response.xpath("//table/tbody/tr")
        #currentDate = self.getCurrentDate()
        currentDate = '23/08/2024'
        for row in rows[1:]:
            columns = row.xpath(".//td")
            dateRaw = self.cleanText(columns[1].xpath(".//text()").get())
            urlAttachRaw = columns[3].xpath(".//a/@href").get()
            date = UtilsMethods.convertDate(dateRaw)
            if date is None or urlAttachRaw is None:
                continue


            if date == currentDate :
                sinopsysRaw = columns[3].xpath(".//a/text()").get()
                urlAttach = self.createUrlAttachField(urlAttachRaw)
                sinopsys = self.cleanText(sinopsysRaw)
                item = TlaxcalaIniciativasItem()
                item['title'] = sinopsys
                item['urlPage'] = response.url
                item['sinopsys'] = sinopsys
                item['federalEstatal'] = "Congreso"
                item['state'] = "Tlaxcala"
                item.set_date_iso(date)
                item['urlAttach'] = urlAttach
                item['collectionName'] = self.name
                yield item

    def createUrlAttachField(self, urlAttach):
        urlAttachArrayList = []
        if urlAttach == None or len(urlAttach) == 0 or urlAttach == 'na':
            urlAttach = 'na'
            return urlAttach

        objAux = {
            'urlAttach': urlAttach,
            'sinopsys': '',
            'wasParsed': 'procesar'
        }
        urlAttachArrayList.append(objAux)
        return urlAttachArrayList

    def getCurrentDate(self):
        spiderDate = getattr(self, 'SPIDER_DATE', None)
        if spiderDate:
            formattedDate = spiderDate
            print("Desde consola: ", formattedDate)
            return formattedDate
        else:
            currentDate = UtilsMethods.getCurrentDateSlashFormatDayMonthYear()
            formattedDate = self.splittedDate(currentDate)
            print("Desde metodo: ", formattedDate)
            return formattedDate

    def cleanText(self, text):
        if text is None or text == '':
            return 'na'

        firstText = UtilsMethods.removeNonBreakingSpace(text)
        secondText = UtilsMethods.removeNewBlankSpace(firstText)
        thirdText = UtilsMethods.removeCharacterText(secondText)
        fourthText = UtilsMethods.cleanFinalText(thirdText)

        textClean = UtilsMethods.stripAccents(fourthText)
        return UtilsMethods.upperCaseText(textClean)
