import scrapy
from datetime import date
from scrapy.exceptions import CloseSpider
from gobierno_scrap.items import QRooPeriodicoOficialItem
from gobierno_scrap.utils.methods import UtilsMethods


class QRooPeriodicoOficialSpider(scrapy.Spider):
    name = "QRooPeriodicoOficial"
    allowed_domains = ["po.segob.qroo.gob.mx"]
    start_urls = ["http://po.segob.qroo.gob.mx/sitiopo/"]

    def parse(self, response):
        urlBaseAttach = "http://po.segob.qroo.gob.mx/sitiopo/"
        currentDate = self.getCurrentDate()
        currentDate="23/12/2024"

        rows = response.css('table tr')
        if len(rows) == 0:
            raise CloseSpider('No hay datos para descargar')

        for row in rows[1:]:
            columns = row.css('td')
            frontPage = self.createUrlAttach(urlBaseAttach, columns[0].css('a::attr(href)').get())
            urlAttachAux = self.createUrlAttach(urlBaseAttach, columns[1].css('a::attr(href)').get())
            urlAttach = self.createUrlAttachField(urlAttachAux)
            dateRaw = self.createDate(columns[2].css('::text').get(), columns[3].css('::text').get(), columns[4].css('::text').get())
            date = UtilsMethods.translateDateForString(dateRaw)
            publicationType = columns[5].css('::text').get()
            number = columns[6].css('::text').get()
            tomo = columns[7].css('::text').get()
            age = columns[8].css('::text').get()
            indexes = columns[9].css('::text').get()
            sinopsys = self.createSinopsys(publicationType, number, tomo, age, indexes)

            if date == currentDate:
                item = QRooPeriodicoOficialItem()
                item['title'] = sinopsys
                item['urlPage'] = response.url
                item['sinopsys'] = self.finalCleanText(sinopsys)
                item['federalEstatal'] = "Estatal"
                item['state'] = "Quintana Roo"
                item.parse_date_str(date)
                item['urlAttach'] = urlAttach
                item['collectionName'] = self.name

                yield item

    def finalCleanText(self, text):
        if UtilsMethods.checkIfTextIsEmpty(text) == '-':
            return '-'

        textClean = UtilsMethods.stripAccents(text)
        return UtilsMethods.upperCaseText(textClean)

    def createUrlAttach(self, urlBase, href):
        newUrl = f"{urlBase}{href}"
        return newUrl

    def createDate(self, day, month, year):
        fullDate = day + "/" + month + "/" + year
        return fullDate

    def createSinopsys(self, publicationType, number, tomo, age, indexes):
        sinopsys = publicationType + " " + number + " " + tomo + " " + age + " " + indexes
        return sinopsys

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
