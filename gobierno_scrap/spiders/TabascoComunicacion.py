import scrapy
from scrapy.exceptions import CloseSpider
from gobierno_scrap.utils.methods import UtilsMethods
from gobierno_scrap.items import TabascoComunicacionItem


class TabascoComunicacionSpider(scrapy.Spider):
    name = "TabascoComunicacion"
    allowed_domains = ["congresotabasco.gob.mx"]
    start_urls = ["https://congresotabasco.gob.mx/boletines/"]

    def parse(self, response):
        arrayListAux = []
        articles = response.xpath("//div//article")
        currentDate = self.getCurrentDate()
        currentDate  = "15/12/2024"
        if len(articles) == 0:
            raise CloseSpider("No se encontraron elementos. Revisar la pagina web.")

        for article in articles[1:]:
            date = article.xpath("./div[2]/*[3]/div/text()").get()
            date = UtilsMethods.dateTabascoComunicacion(date)
            if date == currentDate:
                title = self.cleanText(article.xpath("./div[2]/h3/a/text()").get())
                link = article.xpath("./div[2]/h3/a/@href").get()
                objAux = {'title': title, 'link': link, 'date': date}
                arrayListAux.append(objAux)

        for index in arrayListAux:
            indexUrl = index['link']
            yield scrapy.Request(url=indexUrl, callback=self.parseSingleData, meta={'itemData': index})

    def parseSingleData(self, response):
        itemData = response.meta['itemData']
        sinopsys = self.cleanText(response.xpath("//div[@class='entry-content']/p/text()").getall())
        dateFinal = self.addZeroDate(itemData['date'])
        item = TabascoComunicacionItem()
        item['title'] = itemData['title']
        item['urlPage'] = response.url
        item['sinopsys'] = sinopsys
        item['federalEstatal'] = "Congreso"
        item['state'] = "Tabasco"
        item.parse_date_str(dateFinal)
        item['urlAttach'] = 'na'
        item['collectionName'] = self.name
        yield item

    def addZeroDate(self, date):
        day, month, year = date.split('/')
        formatDate = f"{int(day):02d}/{month}/{year}"
        return formatDate

    def stringTranslateDate(self, currentDate):
        day, month, year = currentDate.split('/')
        formatDate = f"{int(day):d}/{month}/{year}"
        return formatDate

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

    def getCurrentDate(self):
        spiderDate = getattr(self, 'SPIDER_DATE', None)  # day/month/year
        if spiderDate:
            date = spiderDate
            formatDate = self.stringTranslateDate(date)
            print("Desde consola: ", formatDate)
            return formatDate
        else:
            dateNow = UtilsMethods.getCurrentDateSlashFormatDayMonthYear()  # day/month/year
            formatDate = self.stringTranslateDate(dateNow)
            print("Desde metodo: ", formatDate)
            return self.stringTranslateDate(formatDate)
