import scrapy
import logging
from scrapy.exceptions import CloseSpider
from selenium.webdriver.common.by import By
from scrapy_selenium import SeleniumRequest
from gobierno_scrap.items import GuanajuatoGacetaItem
from gobierno_scrap.utils.methods import UtilsMethods
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GuanajuatoGacetaSpider(scrapy.Spider):
    name = "GuanajuatoGaceta"
    allowed_domains = ["www.congresogto.gob.mx"]
    start_urls = ["https://www.congresogto.gob.mx/gaceta_parlamentaria"]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=5)

    def parse(self, response):
        driver = response.request.meta['driver']
        dateScrap = self.getDatePage(driver)
        currentDate = self.getCurrentDate()
        currentDate = "07/10/2024"
        dateScrap = "07/10/2024"

        if dateScrap != currentDate:
            raise CloseSpider('No existen datos con esta fecha...')

        table = response.css('table.table.table-striped tr')
        if len(table) == 0:
            raise CloseSpider('No hay datos o el HTML ha cambiado... Revisar la pagina manualmente')

        for row in table[1:]:
            item = self.extractDataFromRow(row, response, dateScrap)
            yield item

    def extractDataFromRow(self, row, response, date):
        columns = row.css('td')
        idData = columns[1].css('::text').get()
        sinopsys = self.cleanText(columns[2].css('::text').getall())
        urlAttachAux = columns[3].css('a::attr(href)').get()
        urlAttach = self.createUrlAttachField(urlAttachAux)

        item = GuanajuatoGacetaItem()
        item['title'] = sinopsys
        item['urlPage'] = response.url
        item['sinopsys'] = sinopsys
        item['federalEstatal'] = 'Congreso'
        item['state'] = 'Guanajuato'
        item.parse_date_str(date)
        item['urlAttach'] = urlAttach
        item['collectionName'] = self.name

        return item

    def getDatePage(self, driver):
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h4.page-header p')))
        if wait is None:
            raise CloseSpider('No se encontro el elemento en el HTML.')
        dateScrap = self.getDateByRegex(driver.find_element(By.CSS_SELECTOR, 'h4.page-header p').text)
        return dateScrap

    def createUrlAttach(self, url):
        urlBaseAttach = "https://www.congresogto.gob.mx/"
        return UtilsMethods.getUrlDocumentAttach(urlBaseAttach, url)

    def cleanText(self, text):
        if text is None or text == '' or text == ' ':
            return 'na'

        firstText = UtilsMethods.convertListToText(text)
        secondText = UtilsMethods.removeNewBlankSpace(firstText)
        thirdText = UtilsMethods.removeNonBreakingSpace(secondText)
        fourthText = UtilsMethods.removeCharacterText(thirdText)

        fiveText = UtilsMethods.stripAccents(fourthText)
        return UtilsMethods.upperCaseText(fiveText)

    def createUrlAttachField(self, urlAttach):
        urlAttachArrayList = []
        if urlAttach == None or len(urlAttach) == 0:
            urlAttach = 'na'
            return urlAttach

        objAux = {
            'urlAttach': urlAttach,
            'sinopsys': '',
            'wasParsed': 'procesar'
        }
        urlAttachArrayList.append(objAux)
        return urlAttachArrayList

    def getDateByRegex(self, dateString):
        dateStringSplit = dateString.split(',')
        dateStringPart = dateStringSplit[1].strip()
        currentDateString = UtilsMethods.translateDateFormatSlashDateMonthYearFullMonthNames(dateStringPart)
        newDateString = self.slashDateFormat(currentDateString)
        return newDateString

    def slashDateFormat(self, dateString):
        dateStringSplitted = dateString.split('-')
        year = dateStringSplitted[0]
        month = dateStringSplitted[1]
        day = dateStringSplitted[2]
        newDate = f"{day}/{month}/{year}"
        return newDate

    def getCurrentDate(self):
        spiderDate = getattr(self, 'SPIDER_DATE', None)
        if spiderDate:
            formattedDate = spiderDate
            print("Desde consola", formattedDate)
            return formattedDate
        else:
            formattedDate = UtilsMethods.getCurrentDateSlashFormatDayMonthYear()
            print("Desde metodo", formattedDate)
            return formattedDate
