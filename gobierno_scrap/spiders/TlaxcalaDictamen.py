import scrapy
from gobierno_scrap.items import TlaxcalaDictamenItem
from gobierno_scrap.utils.methods import UtilsMethods


class TlaxcaladictamenSpider(scrapy.Spider):
    name = "TlaxcalaDictamen"
    allowed_domains = ["congresodetlaxcala.gob.mx"]
    start_urls = ["https://congresodetlaxcala.gob.mx/dictamenes-2024/"]

    def parse(self, response):
        rows = response.xpath("//table/tbody/tr")
        #currentDate = self.getCurrentDate()
        currentDate = '29/08/2024'
        for row in rows[1:]:
            columns = row.xpath(".//td")
            dateRaw = self.cleanText(columns[0].xpath(".//text()").get())
            #if(dateRaw=="na"): dateRaw=None
            urlAttachRaw = columns[1].xpath(".//a/@href").get()
            if dateRaw is None or urlAttachRaw is None:
                continue

            date = UtilsMethods.translateDateForStringTlaxcalaDictamen(dateRaw)
            print('date ' + date )

            if date == currentDate :
                sinopsysRaw = columns[1].xpath(".//a/text()").get()
                urlAttach = self.createUrlAttachField(urlAttachRaw)
                sinopsys = self.cleanText(sinopsysRaw)
                item = TlaxcalaDictamenItem()
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
