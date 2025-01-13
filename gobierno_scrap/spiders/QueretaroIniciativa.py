import scrapy
import logging
from datetime import date
from scrapy.exceptions import CloseSpider
from gobierno_scrap.utils.methods import UtilsMethods
from gobierno_scrap.items import QueretaroIniciativaItem


class QueretaroIniciativaSpider(scrapy.Spider):
    name = "QueretaroIniciativa"
    allowed_domains = ["legislaturaqueretaro.gob.mx"]
    start_urls = ["http://legislaturaqueretaro.gob.mx/iniciativas/"]

    def parse(self, response):
        urlBaseAttach = 'https://site.legislaturaqueretaro.gob.mx/'

        try:
            rows = response.css('table#supsystic-table-165 tr')
        except:
            raise CloseSpider('Fallo al obtener los datos de la pagina')

        if len(rows) == 0:
            raise CloseSpider('No hay datos en la tabla o el html ha cambiado')

        for row in rows[1:10]:
            columns = row.css('td')
            if len(columns) > 0:
                number = columns[0].css('::text').get().strip()
                date = self.getCurrentDate()
                sinopsys = self.cleanText(columns[1].css('::text').get())
                urlAttachAux = self.checkUrlAttach(urlBaseAttach, columns[2].css('a::attr(href)').get())
                urlAttach = self.createUrlAttachField(urlAttachAux)

                item = QueretaroIniciativaItem()
                item['title'] = '-'
                item['urlPage'] = response.url
                item['sinopsys'] = self.finalCleanText(sinopsys)
                item['federalEstatal'] = 'Estatal'
                item['state'] = 'Queretaro'
                item.parse_date_str(date)
                item['urlAttach'] = urlAttach
                item['collectionName'] = self.name

                yield item

    def finalCleanText(self, text):
        if UtilsMethods.checkIfTextIsEmpty(text) == '-':
            return '-'

        textClean = UtilsMethods.stripAccents(text)
        return UtilsMethods.upperCaseText(textClean)

    def cleanText(self, text):
        text = text.strip()
        firstText = UtilsMethods.removeNewBlankSpace(text)
        secondText = UtilsMethods.removeNonBreakingSpace(firstText)
        thirdText = UtilsMethods.removeCharacterText(secondText)
        return thirdText

    def checkUrlAttach(self, urlBaseAttach, urlAttach):
        if UtilsMethods.startWithHttpMethod(urlAttach):
            return urlAttach

        return UtilsMethods.getUrlDocumentAttach(urlBaseAttach, urlAttach)

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
