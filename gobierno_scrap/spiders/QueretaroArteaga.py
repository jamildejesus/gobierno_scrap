import scrapy
from datetime import date
from gobierno_scrap.items import QueretaroArteagaItem
from datetime import datetime


class QueretaroArteagaSpider(scrapy.Spider):
    name = "QueretaroArteaga"
    allowed_domains = ["lasombradearteaga.segobqueretaro.gob.mx"]
    current_year = str(datetime.now().year) + ".html"
    start_urls = ["https://lasombradearteaga.segobqueretaro.gob.mx/"+current_year]
  

    def parse(self, response):
        current_date = self.getCurrentDate()
        tds = response.xpath('//td')
        index = 0
        list_moth  = [0,0,0,0,0,0,0,0,0,0,0,0]
        for td in tds:
            month = td.xpath('.//text()').get()
            index = index + 1

            if(month=="Enero"):
                list_moth[0]= index
            
            if(month=="Febrero"):
                list_moth[1]= index

            if(month=="Marzo"):
                list_moth[2]= index

            if(month=="Abril"):
                list_moth[3]= index

            if(month=="Mayo"):
                list_moth[4]= index

            if(month=="Junio"):
                list_moth[5] = index

            if(month=="Julio"):
                list_moth[6]= index
            
            if(month=="Agosto"):
                list_moth[7]= index
            
            if(month=="Septiembre"):
                list_moth[8]= index

            if(month=="Octubre"):
                list_moth[9]= index
        
            if(month=="Noviembre"):
                list_moth[10]= index

            if(month=="Diciembre"):
                list_moth[11]= index

        current_month = current_date.month
        current_day = str(current_date.day)
        if current_month  == 12:
            tds = tds[list_moth[current_month-1]:]
        if current_month < 12:
            tds = tds[list_moth[current_month-1]:list_moth[current_month]]

        for td in tds:
            cell_day = td.xpath('.//text()').get()
            href_value = td.xpath('.//a/@href').get()
            if cell_day == current_day and href_value is not None:
                href_value = href_value.replace('../', '', 1)
                new_url = "https://lasombradearteaga.segobqueretaro.gob.mx/" + href_value
                yield scrapy.Request(
                url=new_url, 
                callback=self.parse_new, 
                meta={'url_original': response.url, 'current_date':current_date.strftime("%d/%m/%Y")} 
            )
                
    def parse_new(self, response):
        url_original = response.meta['url_original']
        hrefs = response.xpath('//a/@href').getall()
        print(hrefs)
        list_urlattach = []
        for href in hrefs:
            http =  "https://lasombradearteaga.segobqueretaro.gob.mx/"
            ua = self.createUrlAttachField(http+href)
            list_urlattach.append(ua)

            item = QueretaroArteagaItem()
            item['title'] = '-'
            item['urlPage'] = response.url
            item['sinopsys'] = 'NA'
            item['federalEstatal'] = 'Estatal'
            item['state'] = 'Queretaro'
            #item['date'] = self.getCurrentDate
            item.parse_date_str(response.meta['current_date'])
            item['urlAttach'] = ua
            item['collectionName'] = self.name
            yield item

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
            formatDate = datetime.strptime(spiderDate, "%d/%m/%Y")
            print("Desde consola: ", spiderDate)
            return formatDate
        else:
            currentDate = date.today()
            formatDate = currentDate.strftime("%d/%m/%Y")
            print("Desde metodo: ", formatDate)
            #return formatDate
            return datetime.strptime("06/12/2024", "%d/%m/%Y")
