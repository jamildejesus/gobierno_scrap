import scrapy

from gobierno_scrap.items import AguascalientesGacetaParlamentariaItem
from gobierno_scrap.utils.methods import UtilsMethods
from datetime import date



class AguascalientesGacetaParlamentaria(scrapy.Spider):
    name = "AguascalientesGacetaParlamentaria"
    allowed_domains = ["congresoags.gob.mx"]
    start_urls = ["https://congresoags.gob.mx/agenda_legislativa/actividades_legislativas"]

    def parse(self, response):
        current_date = self.getCurrentDate()
        current_date = "20/12/2024"
        agendas = [
            "//div[@id='tabs-66']//table[@id='datatable-agenda']//tbody/tr",
            "//div[@id='tabs-65']//table[@id='datatable-agenda1']//tbody/tr",
            "//div[@id='tabs-64']//table[@id='datatable-agenda2']//tbody/tr"
        ]
        i=0
        while(i<len(agendas)):
            rows = response.xpath(agendas[i])
            for row in rows:
                tds = row.xpath(".//td")
                num_agenda = tds[0].xpath("text()").get()
                tipo_promocion = tds[1].xpath("text()").get()
                contenido = tds[2].xpath("text()").get()
                fecha = tds[3].xpath(".//span/text()").get()
                recurso = tds[5].xpath(".//a/@href").get()
                urls = []
                urls.append(recurso)
                if current_date == self.raw_date(fecha):
                    print(recurso)
                    item = AguascalientesGacetaParlamentariaItem()
                    item['title'] =  "{0} {1}".format(num_agenda, tipo_promocion)
                    item['urlPage'] = self.start_urls[0]
                    item['sinopsys'] = contenido
                    item['federalEstatal'] = 'Estatal'
                    item['state'] = 'Aguascalientes'
                    item.parse_date_str(current_date)
                    if(recurso):
                        item['urlAttach'] = self.createUrlAttachField(recurso)
                    item['collectionName'] = self.name
                    yield item

                #Tengo los datos requeridos
            i = i + 1;    

    def raw_date(self, date_raw:str):
        if date_raw == "": return None
        if date_raw != None:
            return "%s/%s/%s" %(date_raw[6:],date_raw[4:6] , date_raw[0:4])
        return None
    
    def createUrlAttachField(self, urlAttach):
        urlAttachArrayList = []
        if urlAttach == None or len(urlAttach) == 0:
            urlAttach = 'na'
            return urlAttach
        
        objAux = {
                'urlAttach': "https://congresoags.gob.mx"+urlAttach,
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
