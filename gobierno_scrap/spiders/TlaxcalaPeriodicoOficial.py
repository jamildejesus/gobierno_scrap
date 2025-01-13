import scrapy
from gobierno_scrap.utils.methods import UtilsMethods
from gobierno_scrap.items import TlaxcalaPeriodicoOficialItem


class TlaxcalaperiodicooficialSpider(scrapy.Spider):
    name = "TlaxcalaPeriodicoOficial"
    allowed_domains = ["periodico.tlaxcala.gob.mx"]
    #start_urls = ["https://periodico.tlaxcala.gob.mx/indices/2023.php"]
    start_urls = ["https://publicaciones.tlaxcala.gob.mx/indices/2024.php"]

    def parse(self, response):
        rows = response.xpath("//table//tr")
        urlBaseAttach = 'https://periodico.tlaxcala.gob.mx/indices/'
        currentDate = self.getCurrentDate()
        currentDate = "2024-11-06"

        for row in rows[1:]:
            columns = row.xpath(".//td")
            date = self.cleanText(columns[0].xpath(".//text()").get())
            if date == currentDate:
                sinopsys = self.cleanText(columns[2].xpath(".//text()").get())
                urlAttachAux = self.createUrlAttach(urlBaseAttach, columns[3].xpath(".//a/@href").get())
                urlAttach = self.createUrlAttachField(urlAttachAux)
                dateFinal = self.stringDashDateFormat(date)
                item = TlaxcalaPeriodicoOficialItem()
                item['title'] = sinopsys
                item['urlPage'] = response.url
                item['sinopsys'] = sinopsys
                item['federalEstatal'] = 'Estatal'
                item['state'] = 'Tlaxcala'
                item.parse_date_str(dateFinal)
                item['urlAttach'] = urlAttach
                item['collectionName'] = self.name

                yield item

    def cleanText(self, text):
        if text is None or text == '':
            return 'na'

        firstText = UtilsMethods.removeNonBreakingSpace(text)
        secondText = UtilsMethods.removeNewBlankSpace(firstText)
        thirdText = UtilsMethods.removeCharacterText(secondText)
        fourthText = UtilsMethods.cleanFinalText(thirdText)
        fithText = self.removeRemaingChar(fourthText)

        textClean = UtilsMethods.stripAccents(fithText)
        return UtilsMethods.upperCaseText(textClean)

    def createUrlAttach(self, urlBaseAttach, urlAttach):
        newUrl = f"{urlBaseAttach}{urlAttach}"
        return newUrl

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

    def removeRemaingChar(self, text):
        if text is None or text == '':
            return 'na'

        newText = text.replace("'", "").replace("\"", "")
        return newText

    def getCurrentDate(self):
        spiderDate = getattr(self, 'SPIDER_DATE', None)  # day/month/year
        if spiderDate:
            date = spiderDate
            formatDate = self.stringSlashDateFormat(date)  # year-month-day
            print("Desde consola: ", formatDate)
            return formatDate
        else:
            currentDate = UtilsMethods.getCurrentDate()
            print("Desde metodo: ", currentDate)
            return currentDate

    def stringSlashDateFormat(self, date):
        day, month, year = date.split('/')
        formatDate = f'{year}-{month}-{day}'
        return formatDate

    def stringDashDateFormat(self, date):
        year, month, day = date.split('-')
        formatDate = f'{day}/{month}/{year}'
        return formatDate
