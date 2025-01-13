# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime
from dateutil import parser


class GobiernoScrapItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BaseScrapItem(scrapy.Item):
    title = scrapy.Field()
    urlPage = scrapy.Field()
    sinopsys = scrapy.Field()
    federalEstatal = scrapy.Field()
    state = scrapy.Field()
    date = scrapy.Field()
    
    def set_date_iso(self, c_date):
        date = datetime.strptime(c_date, "%d/%m/%Y")
        date = date.strftime("%Y-%m-%d")
        self["date"] = parser.parse(date)

    def parse_date_str(self, c_date):
        date = datetime.strptime(c_date, "%d/%m/%Y")
        date = date.strftime("%Y-%m-%d")
        self["date"] = parser.parse(date)

class CdmxGacetaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class EdomexGacetaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class GuanajuatoGacetaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class QRooGacetaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class NLPeriodicoOficialItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class NLIniciativaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class QueretaroIniciativaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class TlaxcalaPeriodicoOficialItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class TlaxcalaDictamenItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

#TlaxcalaIniciativasItem
class TlaxcalaIniciativasItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

    
class TlaxcalaDecretoItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class TabascoIniciativaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class TabascoDictamenItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class TabascoGacetaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()


class TabascoComunicacionItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

    

class TabascoPeriodicoOficialItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class QRooIniciativaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()


class QRooPeriodicoOficialItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()


class CampecheGacetaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

    
class CampechePeriodicoOficialItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

    
class CampecheIniciativasItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

    
class AguascalientesIniciativaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class AguascalientesGacetaParlamentariaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()

class QueretaroArteagaItem(BaseScrapItem):
    date = scrapy.Field()
    urlAttach = scrapy.Field()
    collectionName = scrapy.Field()
    





