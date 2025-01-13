import scrapy
from scrapy.exceptions import CloseSpider
from gobierno_scrap.utils.methods import UtilsMethods
from gobierno_scrap.items import TabascoGacetaItem


class TabascoGacetaSpider(scrapy.Spider):
    name = "TabascoGaceta"
    allowed_domains = ["congresotabasco.gob.mx"]
    start_urls = ["https://congresotabasco.gob.mx/gaceta-legislativa/"]

    def parse(self, response):
        rows = response.xpath("//table//tbody//tr")
        currentDate = self.getCurrentDate()
        currentDate = "21/11/2024"
        if len(rows) == 0:
            raise CloseSpider('No hay datos para procesar... Revisa la pagina')

        for row in rows:
            columns = row.xpath(".//td")
            date = self.cleanText(columns[3].xpath(".//text()").get())
            if currentDate == date:
                urlAttachAux = columns[6].xpath(".//a/@href").get()
                urlAttach = self.createUrlAttachField(urlAttachAux)
                item = TabascoGacetaItem()
                item['title'] = 'na'
                item['urlPage'] = response.url
                item['sinopsys'] = 'na'
                item['federalEstatal'] = "Congreso"
                item['state'] = "Tabasco"
                item.set_date_iso(date)
                item['urlAttach'] = urlAttach
                item['collectionName'] = self.name
                yield item

    def cleanText(self, text):
        if text is None or text == '':
            return 'na'

        firstText = UtilsMethods.removeNonBreakingSpace(text.strip())
        secondText = UtilsMethods.removeNewBlankSpace(firstText.strip())
        thirdText = UtilsMethods.removeCharacterText(secondText.strip())
        fourthText = UtilsMethods.cleanFinalText(thirdText.strip())

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
