import os
from datetime import datetime
import sys
import time
import logging
import urllib3
from datetime import date
from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilDate import UtilDate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dateutil import parser



class CdmxPeriodicoOficial():
    def __init__(self, currentDate):
        options = Options()
        options.binary = r"/usr/bin/firefox"
        #options.binary = r'/snap/firefox/current/usr/lib/firefox/firefox'
        options.add_argument('--headless')
        #self.driver = webdriver.Firefox(options=options)
        self.driver = Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        #self.client = MongoClient("mongodb://ws2-db-user:g*B5dk5BuIbAJKd$@172.31.44.17:27017/")
        self.client = MongoClient("mongodb://ws2-db-user:g*B5dk5BuIbAJKd$@127.0.0.1:27017/")

        self.db = self.client['gobierno_scraping']
        self.collection = self.db['resource_collection']
        self.collectionName = "CdmxPeriodicoOficial"
        self.currentDate = currentDate
        logging.basicConfig(level=logging.INFO)

    def startScraping(self):
        url = "https://data.consejeria.cdmx.gob.mx/BusquedaGaceta/operation/BusquedaGaceta.zul"
        self.parse(url)

    def parse(self, url):
        self.driver.get(url)
        time.sleep(8)


        WebDriverWait(self.driver, 5).until(lambda d: d.execute_script("return document.readyState") == "complete")
        print("La página está completamente cargada.")
        elemento = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(@class, 'z-tab-text') and contains(text(), 'POR FECHA')]")))
        elemento.click()
        print("Se hizo clic en el elemento 'POR FECHA'")

        ultimo_input = self.driver.find_element(By.XPATH, "(//input[@class='z-datebox-input'])[last()]")
        self.driver.execute_script("arguments[0].removeAttribute('readonly')", ultimo_input)
        ultimo_input.send_keys(self.currentDate)


        img_element = WebDriverWait(self.driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "(//img[contains(@src, '/BusquedaGaceta/images/buscar.png')])[2]")))
        img_element.click()

        img_elements = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//img[@class='z-button-image' and @src='/BusquedaGaceta/images/pdf-16.png']")))

        i=0;

        t = len(img_elements)

        while(i<t):
            btn_pdf = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//img[@class='z-button-image' and @src='/BusquedaGaceta/images/pdf-16.png']")))[i]
            self.driver.execute_script("arguments[0].click();", btn_pdf)
            time.sleep(20)
            newUrl = self.driver.current_url
            i = i +1
        
        window_handles = self.driver.window_handles
        urls = []
        for handle in window_handles:
            self.driver.switch_to.window(handle)
    
            current_url = self.driver.current_url
            print(f"URL de la pestaña: {current_url}")
            urls.append(current_url)


        #date = self.currentDate
        #if date == self.currentDate:
        for u in urls[1:]:
            urlAttach = self.createUrlAttachField(u)
            item = {
                'title': 'na',
                'urlPage': url,
                'sinopsys': 'na',
                'federalEstatal': 'Estatal',
                'state': 'Cdmx',
                'date': self.set_date_iso(self.currentDate),
                'urlAttach': urlAttach,
                'collectionName': self.collectionName
            }
            self.saveDocument(item)
    
    def set_date_iso(self, c_date):
        date = datetime.strptime(c_date, "%d-%m-%Y")
        date = date.strftime("%Y-%m-%d")
        return  parser.parse(date)

    def createUrlAttachField(self, urlAttach):
        urlAttachArrayList = []
        if len(urlAttach) == 0 or urlAttach == None:
            urlAttach = 'na'
            return urlAttach

        objAux = {
            'urlAttach': urlAttach,
            'sinopsys': '',
            'wasParsed': 'procesar'
        }
        urlAttachArrayList.append(objAux)
        return urlAttachArrayList

    def dateSlashFormat(self, dateString):
        dateSplit = dateString.split('-')
        day = dateSplit[2]
        month = dateSplit[1]
        year = dateSplit[0]
        newDate = f"{day}/{month}/{year}"
        return newDate

    def saveDocument(self, document):
        try:
            self.collection.insert_one(document)
            logging.info(f" Documento guardado correctamente")
        except Exception as e:
            logging.error(f"Error al insertar en la base de datos: {e}")


def is_today():
    return datetime.now().strftime('%Y-%m-%d')

if __name__ == "__main__":
    formatDate = ''
    if len(sys.argv) == 2:
        formatDate = sys.argv[1]
        print('Desde consola:', formatDate)
    else:
        dateNow = date.today()
        formatDate = dateNow.strftime("%d/%m/%Y")
        #formatDate = "08/02/2024"

        print('Desde metodo:', formatDate)
    formatDate="26/11/2024"
    formatDate = datetime.strptime(formatDate, '%d/%m/%Y').strftime('%d-%m-%Y')

    CdmxPeriodicoOficial(currentDate=formatDate).startScraping()
