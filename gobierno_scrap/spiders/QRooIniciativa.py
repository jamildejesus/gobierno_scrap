import scrapy
import logging
from datetime import date
from scrapy.exceptions import CloseSpider
from gobierno_scrap.items import QRooIniciativaItem
from gobierno_scrap.utils.methods import UtilsMethods

# Por subir al server


class QRooIniciativaSpider(scrapy.Spider):
    name = "QRooIniciativa"
    allowed_domains = ["www.congresoqroo.gob.mx"]
    start_urls = ["https://www.congresoqroo.gob.mx/iniciativas/"]

    def parse(self, response):
        rows = response.xpath("//div[@class='section']//ul//li//div//ul[@class='collection coleccion']//li[@class='collection-item'][position()<100]")
        currentDate = self.getCurrentDate()
        currentDate =  "25/11/2024"
        if len(rows) == 0:
            raise CloseSpider('No hay datos para descargar')

        for row in rows:
            rawDate = row.xpath(".//div[@class='row']//span[contains(@class, 'fecha-documento')]/text()").getall()
            date = self.cleanText(rawDate) or 'na'
            if date == 'na':
                continue

            finalDate = self.translateSlashDate(date.strip())
            if finalDate == currentDate:
                title = self.cleanText(row.css('div.row p a::text').get())
                bodyText = self.cleanText(row.css('div.row p a::text').get())
                secondPart = self.cleanText(row.css('span.etiqueta.etiqueta-chica::text').getall())
                sinopsys = f"{bodyText} - {secondPart}"
                urlAttachAux = row.css('div.row p a::attr(href)').get()
                urlAttach = self.createUrlAttachField(urlAttachAux)

                item = QRooIniciativaItem()
                item['title'] = title
                item['urlPage'] = response.url
                item['sinopsys'] = self.finalCleanText(sinopsys)
                item['federalEstatal'] = 'Estatal'
                item['state'] = 'Quintana Roo'
                item.parse_date_str(finalDate)
                item['urlAttach'] = urlAttach
                item['collectionName'] = self.name

                yield item

    def finalCleanText(self, text):
        if UtilsMethods.checkIfTextIsEmpty(text) == '-':
            return '-'

        textClean = UtilsMethods.stripAccents(text)
        return UtilsMethods.upperCaseText(textClean)

    def checkIfTextIsEmpty(self, text):
        if text == '' or text == " " or text == "&nbsp;":
            return True

        return False

    def cleanText(self, text):
        if self.checkIfTextIsEmpty(text):
            return 'na'

        return UtilsMethods.convertListToText(text)

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

    def translateSlashDate(self, dateString):
        dateCleanComma = dateString.replace('.', '').replace(',', '')
        newDateString = UtilsMethods.dateQRooIniciativaDateSplit(dateCleanComma)
        return newDateString
