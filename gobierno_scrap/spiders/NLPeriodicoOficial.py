import scrapy
import logging
from datetime import date
from gobierno_scrap.utils.methods import UtilsMethods
from gobierno_scrap.items import NLPeriodicoOficialItem


class NLPeriodicoOficialSpider(scrapy.Spider):
    name = "NLPeriodicoOficial"
    allowed_domains = ["sgi.nl.gob.mx"]
    start_urls = [
        #"http://sgi.nl.gob.mx/Transparencia_2015/Acciones/PeriodicoOficial.aspx"
        "https://sistec.nl.gob.mx/Transparencia_2015_LyPOE/Acciones/PeriodicoOficial.aspx"
    ]

    def parse(self, response):
        rows = response.css('#dgData tr')
        currentDate = self.getCurrentDate()
        currentDate = '18/12/2024'

        for row in rows[1:]:
            columns = row.css('td')

            if (len(columns) == 0):
                raise ("No hay datos para obtener o el html cambio")

            if (len(columns) > 1):
                numberDoc = columns[0].css('::text').get() or "-"
                dateRaw = columns[1].css('::text').get() or "na"
                date = self.buildCorrectDate(dateRaw)
                urlAttachAux = columns[2].css('a::attr(href)').getall()
                urlAttach = self.createUrlAttachField(urlAttachAux)
                exampleData = columns[3].css('a::attr(href)').getall()
                if date == currentDate:
                    print("Let's go")
                    item = NLPeriodicoOficialItem()
                    item['title'] = "na"
                    item['urlPage'] = self.start_urls[0]
                    item['sinopsys'] = "na"
                    item['federalEstatal'] = "Estatal"
                    item['state'] = "Nuevo Leon"
                    item.parse_date_str(date)
                    #item.set_date_iso(date)
                    item['urlAttach'] = urlAttach
                    item['collectionName'] = self.name
                    print("Saving date....")
                    yield item

    def createUrlAttachField(self, urlAttach):
        urlAttachArrayList = []
        if urlAttach == None or len(urlAttach) == 0:
            urlAttach = 'na'
            return urlAttach

        for url in urlAttach:
            objAux = {
                'urlAttach': url.replace("http://", "https://"),
                'sinopsys': '',
                'wasParsed': 'procesar'
            }
            urlAttachArrayList.append(objAux)
        return urlAttachArrayList

    def buildCorrectDate(self, year):
        newDate = UtilsMethods.dateFormatSlashDateMonthYearFullMonthNames(year)
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
