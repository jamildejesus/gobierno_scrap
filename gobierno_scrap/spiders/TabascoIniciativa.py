import scrapy
from gobierno_scrap.utils.methods import UtilsMethods
from gobierno_scrap.items import TabascoIniciativaItem


class TabascoIniciativaSpider(scrapy.Spider):
    name = "TabascoIniciativa"
    allowed_domains = ["congresotabasco.gob.mx"]
    start_urls = ["https://congresotabasco.gob.mx/iniciativas/"]

    def parse(self, response):
        rows = response.xpath("//table//tbody//tr")
        currentDate = self.getCurrentDate()
        currentDate="21/11/2024"

        for row in rows:
            columns = row.xpath(".//td")
            title = self.cleanText(columns[1].xpath('.//text()').get())
            date = columns[4].xpath('.//text()').get()
            urlAttachAux = columns[7].xpath('.//p/a/@href').get()
            urlAttach = self.createUrlAttachField(urlAttachAux)
            if date == currentDate:
                item = TabascoIniciativaItem()
                item['title'] = title
                item['urlPage'] = response.url
                item['sinopsys'] = title
                item['federalEstatal'] = 'Congreso'
                item['state'] = 'Tabasco'
                item.set_date_iso(date)
                item['urlAttach'] = urlAttach
                item['collectionName'] = self.name
                print("Data saved")
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
