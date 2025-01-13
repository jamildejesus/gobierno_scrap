import re
import scrapy
from gobierno_scrap.utils.methods import UtilsMethods
from gobierno_scrap.items import EdomexGacetaItem


class EdomexGacetaSpider(scrapy.Spider):
    name = "EdomexGaceta"
    allowed_domains = ["legislacion.legislativoedomex.gob.mx"]
    #start_urls = ["https://legislacion.legislativoedomex.gob.mx/gaceta"]
    start_urls = ["https://legislacion.legislativoedomex.gob.mx/asuntosparlamentarios/gaceta"]

    def parse(self, response):
        currentDate = self.getCurrentDate()
        #currentDate = "28/11/2024"
        firstData = response.xpath("//div[@id='contenido_left']//div[@style='float: left;']")
        dateRaw = self.cleanText(firstData.xpath(".//p/span/text()").get())
        date = self.getDateFromRegex(dateRaw.lower())
        if date == currentDate:
            urlAux = self.getUrlByRegex(firstData.xpath(".//button").get())
            urlAttach = self.createUrlAttachField(urlAux)
            item = EdomexGacetaItem()
            item['title'] = 'na'
            item['urlPage'] = response.url
            item['sinopsys'] = 'na'
            item['federalEstatal'] = 'Congreso'
            item['state'] = 'EdoMex'
            item.parse_date_str(date)
            item['urlAttach'] = urlAttach
            item['collectionName'] = self.name
            yield item        
        else:
            secondData = response.xpath("//div[@id='contenido_left']//a")
            for index in secondData:
                dateRawSecondData = self.cleanText(index.xpath(".//div[@class='ley_name']/b/text()").get())
                dateSeconData = self.getDateFromRegex(dateRawSecondData.lower())
                if dateSeconData != currentDate:
                    continue

                urlAttachAux = index.xpath(".//@href").get()
                urlAttach = self.createUrlAttachField(urlAttachAux)
                item = EdomexGacetaItem()
                item['title'] = 'na'
                item['urlPage'] = response.url
                item['sinopsys'] = 'na'
                item['federalEstatal'] = 'Congreso'
                item['state'] = 'EdoMex'
                item.set_date_iso(dateSeconData)
                item['urlAttach'] = urlAttach
                item['collectionName'] = self.name
                yield item

    def getUrlByRegex(self, html):
        pattern = r"window\.open\('([^']+)'\)"
        match = re.search(pattern, html)
        if match:
            url = match.group(1)
            return url

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

    def getDateFromRegex(self, text):
        pattern = r'(\d{2}) de ([^\d,]+), (\d{4})'
        match = re.match(pattern, text)
        if match:
            day = match.group(1)
            month = match.group(2)
            year = match.group(3)
            fullYear = f"{day}/{month}/{year}"
            return UtilsMethods.translateDateForString(fullYear)

    def getCurrentDate(self):
        spiderDate = getattr(self, 'SPIDER_DATE', None)
        if spiderDate:
            date = spiderDate
            print("Desde consola: ", date)
            return date
        else:
            currentDate = UtilsMethods.getCurrentDateSlashFormatDayMonthYear()
            print("Desde metodo: ", currentDate)
            return currentDate

    def stringSlashDateFormat(self, date):
        if '-' in date:
            day, month, year = date.split('-')
            formatDate = f'{day}/{month}/{year}'
            return formatDate
        else:
            return date
