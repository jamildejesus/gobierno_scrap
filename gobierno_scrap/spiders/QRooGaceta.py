import scrapy
from datetime import date
from scrapy.exceptions import CloseSpider

from gobierno_scrap.items import QRooGacetaItem
from gobierno_scrap.utils.methods import UtilsMethods


class QRooGacetaSpider(scrapy.Spider):
    name = "QRooGaceta"
    allowed_domains = ["gacetaparlamentaria.congresoqroo.gob.mx", "congresoqroo.gob.mx"]
    #urlBaseAttach = "https://gacetaparlamentaria.congresoqroo.gob.mx/gaceta/68"
    urlBaseAttach = "https://gacetaparlamentaria.congresoqroo.gob.mx/gaceta/277"

    def start_requests(self):
        dayRequest, monthRequest, yearRequest = self.getCurrentDate().split('/')
        dayRequest = 31
        monthRequest = 10
        yearRequest = 2024
        urlRequest = f"https://congresoqroo.gob.mx/api/v1/gaceta/?mes={monthRequest}&format=json&anio={yearRequest}"
        dateRequest = f"{monthRequest}/{yearRequest}"
        yield scrapy.Request(url=urlRequest, callback=self.parseIdItem, meta={'dateRequest': dateRequest})

    def parseIdItem(self, response):
        currentDate = self.getCurrentDate()
        currentDate = '31/10/2024'
        if response.status != 200:
            raise CloseSpider('No se encontro el elemento en la respuesta.')

        data = response.json()
        objDataRequest = self.buildObjectDataRequest(data, currentDate)
        urlRequestSingleRequest = f"https://congresoqroo.gob.mx/api/v1/gaceta/{objDataRequest['id']}/doctos?format=json"
        yield scrapy.Request(url=urlRequestSingleRequest, callback=self.parse, meta={'itemData': objDataRequest})

    def buildObjectDataRequest(self, data, currentDate):
        for item in data:
            idItem = item['id']
            datePublish = self.translateSlashDate(item['fecha_publicacion'])
            if datePublish == currentDate:
                objDataRequest = {
                    'id': idItem,
                    'date': datePublish
                }
                return objDataRequest

    def parse(self, response):
        itemData = response.request.meta['itemData']
        if response.status != 200:
            raise CloseSpider('No se encontro el elemento en la respuesta.')

        data = response.json()
        if len(data) == 0:
            raise CloseSpider('No hay datos en la respuesta. Revisar el HTML para mas informacion.')

        for item in data:
            sinopsys = self.finalCleanText(item['titulo'])
            urlAttach = self.createUrlAttachField(item['url'])
            items = QRooGacetaItem()
            items['title'] = sinopsys
            items['urlPage'] = response.url
            items['sinopsys'] = sinopsys
            items['federalEstatal'] = "Estatal"
            items['state'] = "Quintana Roo"
            items.parse_date_str(itemData['date'])
            items['urlAttach'] = urlAttach
            items['collectionName'] = self.name
            yield items

    def finalCleanText(self, text):
        if UtilsMethods.checkIfTextIsEmpty(text) == '-':
            return 'na'

        textClean = UtilsMethods.stripAccents(text)
        return UtilsMethods.upperCaseText(textClean)

    def createUrlAttachField(self, urlAttach):
        urlAttachArrayList = []
        if urlAttach == None or len(urlAttach) == 0 or urlAttach == 'na' or urlAttach == '':
            urlAttach = 'na'
            return urlAttach

        objAux = {
            'urlAttach': urlAttach,
            'sinopsys': '',
            'wasParsed': 'procesar'
        }
        urlAttachArrayList.append(objAux)
        return urlAttachArrayList

    def translateSlashDate(self, dateRaw):
        year, month, day = dateRaw.split('-')
        return f'{day}/{month}/{year}'

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

    def buildNewDate(self, dateCalendar, monthRequest, yearRequest):
        newDate = f'{int(dateCalendar):02d}/{monthRequest}/{yearRequest}'
        return newDate
