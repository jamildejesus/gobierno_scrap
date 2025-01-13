import scrapy
import logging
from datetime import date
from scrapy.exceptions import CloseSpider
from gobierno_scrap.items import NLIniciativaItem
from gobierno_scrap.utils.methods import UtilsMethods


class NLIniciativaSpider(scrapy.Spider):
    name = "NLIniciativa"
    allowed_domains = [""]
    start_urls = [
        "https://www.hcnl.gob.mx/trabajo_legislativo/iniciativas/pan.php",
        "https://www.hcnl.gob.mx/trabajo_legislativo/iniciativas/pri.php",
        "https://www.hcnl.gob.mx/trabajo_legislativo/iniciativas/morena.php",
        "https://www.hcnl.gob.mx/trabajo_legislativo/iniciativas/pt.php",
        "https://www.hcnl.gob.mx/trabajo_legislativo/iniciativas/pmc.php",
        "https://www.hcnl.gob.mx/trabajo_legislativo/iniciativas/pvem.php",
        "https://www.hcnl.gob.mx/trabajo_legislativo/iniciativas/pes.php",
        "https://www.hcnl.gob.mx/trabajo_legislativo/iniciativas/panal.php",
        "https://www.hcnl.gob.mx/trabajo_legislativo/iniciativas/prd.php",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urlBaseAttach = "https://www.hcnl.gob.mx/"
        currentDate = self.getCurrentDate()
        currentDate = "06/11/2024"
        rows = response.css("div.tab-pane.active table tr")

        if len(rows) <= 1:
            logging.debug("No se encontraron resultados")
            raise CloseSpider("No se encontraron resultados")

        for row in rows[1:]:
            columns = row.css('td')
            expediente = columns[0].css('::text').get()
            title = self.cleanText(columns[1].css('a::text').get())
            comission = self.cleanText(columns[2].css('::text').get())
            date = columns[3].css('::text').get()

            if date == currentDate:
                status = self.cleanText(columns[4].css('::text').getall())
                urlAttachAux = self.createUrlAttach(urlBaseAttach, columns[5].css('a::attr(href)').get())
                urlAttach = self.createUrlAttachField(urlAttachAux)

                item = NLIniciativaItem()
                item['title'] = title
                item['urlPage'] = response.url
                item['sinopsys'] = self.finalCleanText(title)
                item['federalEstatal'] = "Estatal"
                item['state'] = "Nuevo Leon"
                item.parse_date_str(date)
                item['urlAttach'] = urlAttach
                item['collectionName'] = self.name
                print("Data saved")
                yield item

    def finalCleanText(self, text):
        if UtilsMethods.checkIfTextIsEmpty(text) == '-':
            return '-'

        textClean = UtilsMethods.stripAccents(text)
        return UtilsMethods.upperCaseText(textClean)

    def cleanText(self, text):
        firstText = UtilsMethods.convertListToText(text)
        secondText = UtilsMethods.checkIfTextIsEmpty(firstText)
        thirdText = UtilsMethods.removeCharacterText(secondText)
        fourthText = UtilsMethods.removeNewBlankSpace(thirdText)
        return UtilsMethods.removeNonBreakingSpace(fourthText.strip())

    def createUrlAttach(self, urlBase, url):
        if UtilsMethods.startWithHttpMethod(url):
            return url

        return UtilsMethods.getUrlDocumentAttach(urlBase, url)

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
