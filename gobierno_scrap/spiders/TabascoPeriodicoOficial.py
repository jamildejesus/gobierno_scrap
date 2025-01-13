import scrapy
from scrapy.exceptions import CloseSpider
from gobierno_scrap.utils.methods import UtilsMethods
from gobierno_scrap.items import TabascoPeriodicoOficialItem


class TabascoPeriodicoOficialSpider(scrapy.Spider):
    name = "TabascoPeriodicoOficial"
    allowed_domains = ["tabasco.gob.mx"]
    start_urls = ["https://tabasco.gob.mx/PeriodicoOficial"]

    def parse(self, response):
        rows = response.xpath("//table//tbody//tr")
        urlBaseAttach = "https://tabasco.gob.mx/"
        currentDate = self.getCurrentDate()
        currentDate = "23/11/2024"

        if len(rows) == 0:
            raise CloseSpider('No hay datos para procesar... Revisa la pagina')

        for row in rows:
            colums = row.xpath(".//td")
            date = UtilsMethods.translateDateFormatSlashDateMonthYear(colums[0].xpath(".//text()").get())
            sinopsys = self.cleanText(colums[4].xpath(".//text()").getall())
            urlAttachAux = UtilsMethods.getUrlDocumentAttach(urlBaseAttach, colums[5].xpath(".//a/@href").get())
            urlAttach = self.createUrlAttachField(urlAttachAux)
            if currentDate == date:
                item = TabascoPeriodicoOficialItem()
                item['title'] = sinopsys
                item['urlPage'] = response.url
                item['sinopsys'] = sinopsys
                item['federalEstatal'] = "Estatal"
                item['state'] = "Tabasco"
                item.parse_date_str(date)
                item['urlAttach'] = urlAttach
                item['collectionName'] = self.name
                yield item

    def cleanText(self, text):
        if text is None or text == '':
            return 'na'

        txtList = UtilsMethods.convertListToText(text)

        firstText = UtilsMethods.removeNonBreakingSpace(txtList)
        secondText = UtilsMethods.removeNewBlankSpace(firstText)
        thirdText = UtilsMethods.removeCharacterText(secondText)
        fourthText = UtilsMethods.cleanFinalText(thirdText)

        textClean = UtilsMethods.stripAccents(fourthText)
        return UtilsMethods.upperCaseText(textClean)

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
            formatteDate = spiderDate
            print(f"Desde consola:", formatteDate)
            return formatteDate
        else:
            formattedDate = UtilsMethods.getCurrentDateSlashFormatDayMonthYear()
            print(f"Desde el metodo:", formattedDate)
            return formattedDate
