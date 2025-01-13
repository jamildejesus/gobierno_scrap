import re
import scrapy
from gobierno_scrap.utils.methods import UtilsMethods
from gobierno_scrap.items import CdmxGacetaItem


class CdmxGacetaSpider(scrapy.Spider):
    name = "CdmxGaceta"
    allowed_domains = ["www.congresocdmx.gob.mx"]
    #start_urls = ["https://www.congresocdmx.gob.mx/gaceta-parlamentaria-206-2.html"]
    start_urls = ["https://www.congresocdmx.gob.mx/gaceta-parlamentaria-iii-legislatura-206-4.html"]
    def parse(self, response):
        urlBaseAttach = 'https://www.congresocdmx.gob.mx/'
        articles = response.xpath("//div[contains(@class, 'u-shadow-v1-3')]//div[@class='media']")
        currentDate = self.getCurrentDate()
        currentDate =  "17-12-2024"
        for article in articles:
            date = self.getDate(article.xpath(".//div[@class='media-body']//span/text()").get())
            if date != currentDate:
                continue

            synopsys = self.cleanText(article.xpath(".//div[@class='media-body']//strong/text()").get())
            urlAttachAux = self.createUrlAttach(urlBaseAttach, article.xpath(".//div//a/@href").get())
            urlAttach = self.createUrlAttachField(urlAttachAux)

            dateFinal = self.stringDashDateFormat(date)

            item = CdmxGacetaItem()
            item['title'] = 'na'
            item['urlPage'] = response.url
            item['sinopsys'] = synopsys
            item['federalEstatal'] = 'Congreso'
            item['state'] = 'Cdmx'
            item.parse_date_str(dateFinal)
            item['urlAttach'] = urlAttach
            item['collectionName'] = self.name
            yield item
    def getDate(self, date):
        pattern = r'\d{2}-\d{2}-\d{4}'
        matches = re.search(pattern, date)
        if matches:
            newDate = matches[0]
            return newDate

    def createUrlAttach(self, urlBaseAttach, urlAttach):
        if urlAttach == ' ' or urlAttach == '':
            return 'na'

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

    def cleanText(self, text):
        if text is None or text == '':
            return 'na'

        firstText = UtilsMethods.removeNonBreakingSpace(text.strip())
        secondText = UtilsMethods.removeNewBlankSpace(firstText.strip())
        thirdText = UtilsMethods.removeCharacterText(secondText.strip())
        fourthText = UtilsMethods.cleanFinalText(thirdText.strip())
        textClean = UtilsMethods.stripAccents(fourthText)
        return UtilsMethods.upperCaseText(textClean)

    def getCurrentDate(self):
        spiderDate = getattr(self, 'SPIDER_DATE', None)
        if spiderDate:
            date = spiderDate
            formatDate = self.stringSlashDateFormat(date)
            print("Desde consola: ", formatDate)
            return formatDate
        else:
            currentDate = UtilsMethods.getCurrentDateDashFormatDayMonthYear()
            print("Desde metodo: ", currentDate)
            return currentDate

    def stringSlashDateFormat(self, date):
        day, month, year = date.split('/')
        formatDate = f'{day}-{month}-{year}'
        return formatDate

    def stringDashDateFormat(self, date):
        day, month, year = date.split('-')
        formatDate = f'{day}/{month}/{year}'
        return formatDate
