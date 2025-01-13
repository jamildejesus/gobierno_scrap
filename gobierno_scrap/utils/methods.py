import re
from unidecode import unidecode
from datetime import date
import datetime

nonWorkingDays = [
    datetime.date.weekday(datetime.date.min + datetime.timedelta(days=5)),
    datetime.date.weekday(datetime.date.min + datetime.timedelta(days=6))
]

monthsShortTranslate = {
    "jan": "ene",
    "feb": "feb",
    "mar": "mar",
    "apr": "abr",
    "may": "may",
    "jun": "jun",
    "jul": "jul",
    "aug": "ago",
    "sep": "sep",
    "oct": "oct",
    "nov": "nov",
    "dec": "dic"
}

monthsNumbers = {
    "ene": "01",
    "feb": "02",
    "mar": "03",
    "abr": "04",
    "may": "05",
    "jun": "06",
    "jul": "07",
    "ago": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dic": "12"
}

monthsFull = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12",
    "ago":"08"
}

monthsMixFullAndShort = {
    "ene": "01",
    "feb": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "ago": "08",
    "sep": "09",
    "oct": "10",
    "nov": "11",
    "dic": "12"
}


class UtilsMethods:

    @staticmethod
    def convertListToText(text):
        if (isinstance(text, list)):
            completeText = ' '.join(text)
            return completeText

        return text

    @staticmethod
    def getUrlDocumentAttach(urlBase, href):
        urlSplit = href.split('/')
        currentUrl = '/'.join(urlSplit[1:])
        newUrl = f"{urlBase}{currentUrl}"
        return newUrl

    @staticmethod
    def removeNewBlankSpace(text):
        if text.strip() == '&nbsp':
            return '-'

        textClean = text.replace('&nbsp;', ' ')
        return textClean

    @staticmethod
    def removeNonBreakingSpace(text):
        textClean = text.replace('\xa0', '').strip()
        return textClean

    @staticmethod
    def removeStrongEmptyTags(text):
        textClean = re.sub(r'<strong>\s*</strong>', '', text)
        return textClean

    @staticmethod
    def checkIfTextIsEmpty(text):
        if text == '' or text == " " or text == "&nbsp;":
            return '-'

        return text

    @staticmethod
    def removeCharacterText(text):
        textClean = text.replace('\r', '').replace('\n', '')
        return textClean

    @staticmethod
    def removeTabCharacter(text):
        textClean = text.replace('\t', '')
        return textClean

    @staticmethod
    def removeSpecialCharacterNLComunicacion(text):
        textClean = text.replace('\r', '').replace('\n', ' ')
        return textClean

    def removeSpecialCharacterSinaloaPeriodicoOficial(text):
        textClean = text.replace('\r', '').replace('\n', ' ').replace('\t', '')
        return textClean

    @staticmethod
    def startWithHttpMethod(url):
        if url.startswith('http') or url.startswith('https'):
            return True

        return False

    def cleanFinalText(text):
        currentText = text.split()
        textClean = ' '.join(currentText)
        return textClean

    def removeBrTag(text):
        textClean = text.replace('<br>', '')
        return textClean

    def removeBracketsCharacter(text):
        textClean = re.sub(r'\{(.*?)\}', r'\1', text)
        return textClean

    def removeEllipsis(text):
        textClean = text.split('...')[0].strip()
        return textClean

    def stripAccents(text):
        textClean = unidecode(text)
        return textClean

    def upperCaseText(text):
        textClean = text.upper()
        return textClean

    @staticmethod
    def isPDFUrl(text):
        if text.endswith('.pdf') or text.endswith('.PDF'):
            return True
        else:
            return False

    @staticmethod
    def getCurrentDate():
        currentDate = date.today()
        formatDate = currentDate.strftime("%Y-%m-%d")
        return formatDate

    def getCurrentDateSlashFormatDayMonthYear():
        currentDate = date.today()
        formatDate = currentDate.strftime("%d/%m/%Y")
        return formatDate

    def getCurrentDateSlashFormatYearMonthDay():
        currentDate = date.today()
        formatDate = currentDate.strftime("%Y/%m/%d")
        return formatDate

    def getCurrentDateDashFormatDayMonthYear():
        currentDate = date.today()
        formatDate = currentDate.strftime("%d-%m-%Y")
        return formatDate

    @staticmethod
    def isCorrectYear(date, yearLimit):
        if date is None or date == '' or date == ' ':
            return False

       # yearLimit = '2023'
        if date.find(yearLimit) != -1:
            return True
        return False

    @staticmethod
    def isSameDate(currentDate, targetDate):
        if currentDate == targetDate:
            return True
        return False

    @staticmethod
    def businessDays(days):
        calendar = datetime.datetime.today()
        index = 0
        while index < abs(days):
            calendar += datetime.timedelta(days=1) if days > 0 else datetime.timedelta(days=-1)
            if calendar.weekday() not in nonWorkingDays:
                index += 1
        return calendar.date()

    @staticmethod
    def formatHypenYearMonthDayDate(date):
        formatDate = date.strftime("%Y-%m-%d")
        return formatDate

    @staticmethod
    def formatHypenDayMonthYearDate(date):
        formatDate = date.strftime("%d-%m-%Y")
        return formatDate

    @staticmethod
    def formatSlashYearMonthDayDate(date):
        formatDate = date.strftime("%Y/%m/%d")
        return formatDate

    @staticmethod
    def formatSlashDayMonthYearDate(date):
        formatDate = date.strftime("%d/%m/%Y")
        return formatDate

    def translateDateFormatSlashDateMonthYear(date):
        day, month, year = date.split('/')
        month = monthsNumbers[month.lower()]
        translatedDate = f"{day}/{month}/{year}"
        return translatedDate

    @staticmethod
    def checkTypeDataInstance(urlAttach):
        typeDataInstance = ''

        if isinstance(urlAttach, str):
            typeDataInstance = 'singleStr'
            return typeDataInstance

        if isinstance(urlAttach, list):
            if all(isinstance(item, dict) for item in urlAttach):
                typeDataInstance = 'dict'
                return typeDataInstance
            elif all(isinstance(item, str) for item in urlAttach):
                typeDataInstance = 'array'
                return typeDataInstance
        return False

    @staticmethod
    def changeMontNameToNumberFormatSlashDayMonthYear(date):
        for monthName, monthNumber in monthsFull.items():
            date = date.replace(monthName, monthNumber)
        dateTranslate = datetime.datetime.strptime(date.strip(), "%d de %m de %Y").strftime("%d/%m/%Y")
        return dateTranslate

    @staticmethod
    def getRegexDate(text):
        matches = re.findall(r'\d{2}\sDE\s\w+\sDE\s\d{4}', text)
        if matches:
            return matches[0]

    @staticmethod
    def getRegexDateLowerFullDate(text):
        match = re.search(r"\d{2} de \w+ de \d{4}", text)
        if match:
            return match[0]

    @staticmethod
    def getRegexDateFormatSlashDayMonthYear(text):
        matches = re.findall(r'\d{2}/\d{2}/\d{4}', text)
        if matches:
            return matches[0]

    @staticmethod
    def getScrapingDateFromUrl(text):
        match = re.search(r"(\d{4}_\d{1,2}/\w+/\d{1,2})", text)
        if match:
            auxDate = match.group(1)
            dateSplit = auxDate.split('/')
            year = dateSplit[0].split('_')[0]
            month = dateSplit[1]
            day = dateSplit[2]
            finalDate = f"{day}/{month}/{year}"
            return finalDate

    def getRegexDateLowerFullDatePueblaGaceta(text):
        match = re.search(r"\d{2} de \w+ del \d{4}", text)
        if match:
            return match.group(0)

    def getRegexSonoraComunicacion(text):
        matchFirst = re.search(r"\w+ \d{1,2} de \d{4}", text)
        matchSecond = re.search(r"\w+ \d{1,2}° de \d{4}", text)
        matchThird = re.search(r"\d{2} de \w+ de \d{4}", text)

        if matchFirst:
            newDate = UtilsMethods.regexDateSonoraComunicacion(matchFirst.group(0))
            return newDate

        if matchSecond:
            cleanDate = matchSecond.group(0).replace('°', '')
            newDate = UtilsMethods.regexDateSonoraComunicacion(cleanDate)
            return newDate

        if matchThird:
            # 28 de agosto de 2023
            newDate = UtilsMethods.dateFormatSlashDateMonthYearFullMonthNames(matchThird.group(0))
            return newDate

    def regexDateSonoraComunicacion(text):
        splitText = text.split(' ')
        month = splitText[0]
        day = splitText[1]
        year = splitText[3]
        monthTranslate = monthsFull[month.lower()]
        translateDate = f"{int(day):02d}/{monthTranslate}/{year}"
        return translateDate

    def translateDateFormatSlashDateMonthYearFullMonthNames(date):
        split_text = date.split(' ')
        day = split_text[0]
        month = split_text[2]
        year = split_text[4]
        month = monthsFull[month.lower()]
        translatedDate = f"{year}-{month}-{day}"
        return translatedDate

    def dateFormatSlashDateMonthYearFullMonthNames(date):
        split_text = date.split(' ')
        day = split_text[0]
        month = split_text[2]
        year = split_text[4]
        month = monthsFull[month.lower()]
        translatedDate = f"{day}/{month}/{year}"
        return translatedDate

    def regexDateSlashTranslate(date):
        split_text = date.split(' ')
        day = split_text[0]
        month = split_text[2]
        year = split_text[4]
        month = monthsFull[month.lower()]
        translatedDate = f"{day}/{month}/{year}"
        return translatedDate

    def regexSplitSpaceDate(date):
        split_text = date.split(' ')
        day = split_text[0]
        month = split_text[1]
        year = split_text[2]
        month = monthsFull[month.lower()]
        translatedDate = f"{day}/{month}/{year}"
        return translatedDate

    def translateDateForString(dateString):
        splitDate = dateString.split('/')
        day = splitDate[0]
        month = splitDate[1]
        year = splitDate[2]
        monthTranslate = monthsFull[month.lower()]
        dateFinal = f"{day}/{monthTranslate}/{year}"
        return dateFinal

    def translateDateDashForString(dateString):
        splitDate = dateString.split('-')
        day = splitDate[0]
        month = splitDate[1]
        year = splitDate[2]
        monthTranslate = monthsNumbers[month.lower()]
        dateFinal = f"{day}/{monthTranslate}/{year}"
        return dateFinal

    def translateDateSlashMonthShortForString(dateString):
        splitDate = dateString.split('/')
        day = splitDate[0]
        month = splitDate[1]
        year = splitDate[2]
        monthTranslate = monthsShortTranslate[month.lower()]
        monthNumber = monthsNumbers[monthTranslate.lower()]
        dateFinal = f"{day}/{monthNumber}/{year}"
        return dateFinal

    def translateDateForStringTlaxcalaDictamen(dateString):
        splitDate = dateString.split('/')
        day = splitDate[0]
        month = splitDate[1].lower()
        year = splitDate[2]

        monthTranslate = monthsFull.get(month.lower(), month)
        dateFinal = f"{day}/{monthTranslate}/{year}"
        return dateFinal

    def monthYearSlashDate(dateString):
        splitText = dateString.split(' ')
        month = splitText[0]
        year = splitText[1]
        monthTranslate = monthsFull[month.lower()]
        finalDate = f"{monthTranslate}/{year}"
        return finalDate

    def buildDate(day, month, year):
        monthTranslate = monthsFull[month.lower()]
        newDate = f"{day}/{monthTranslate}/{year}"
        return newDate

    def dateTabascoComunicacion(dateString):
        dateSplit = dateString.split()
        day = dateSplit[0]
        month = dateSplit[1][:-1]
        year = dateSplit[2]
        monthTranslate = monthsFull[month.lower()]
        newDate = f"{day}/{monthTranslate}/{year}"
        return newDate

    def dateNLComunicacionSplit(date):
        split_text = date.split(' ')
        day = split_text[0]
        month = split_text[2]
        year = split_text[3]
        month = monthsFull[month.lower()]
        translatedDate = f"{int(day):02d}/{month}/{year}"
        return translatedDate

    def dateQRooIniciativaDateSplit(date):
        dateSplit = date.split(' ')
        month = dateSplit[0]
        day = dateSplit[1]
        year = dateSplit[2]
        monthTranslate = monthsMixFullAndShort[month.lower()]
        translateDate = f"{int(day):02d}/{monthTranslate}/{year}"
        return translateDate

    def sinaloaComunicacionDateSplit(date):
        dateSplit = date.split(' ')
        month = dateSplit[0]
        day = dateSplit[1]
        year = dateSplit[2]
        monthTranslate = monthsFull[month.lower()]
        return f"{int(day):02d}/{monthTranslate}/{year}"

    def dateFormatSlashDateMonthYearFullMonthNamesV2(date):
        if date is None:
            return "na"
        split_text = date.split(' ')
        day = split_text[0]
        month = split_text[2]
        year = split_text[3]
        month = monthsFull[month.lower()]
        translatedDate = f"{day}/{month}/{year}"
        return translatedDate

    @staticmethod
    def regexTextDate(text):
        text = text.upper()
        match = re.findall(r".*\s(\d{1,2} DE [A-Z]+ \d{4})", text)
        if match:
            return match[0]


    @staticmethod
    def getUrlDocumentAttachV2(urlBase, href):
        urlSplit = href.split('/')
        currentUrl = '/'.join(urlSplit[:])
        newUrl = f"{urlBase}{currentUrl}"
        return newUrl
    
    # 05-01-24  dd-mm-yy
    def convertDate(date:str) -> str | None:
        regex:str = r'^(0[1-9]|1[0-9]|2[0-9]|3[01])-(0[1-9]|1[0-2])-(\d{2})$' 
        evaluate:re.Match = re.match(regex, date)
        if(isinstance(evaluate, re.Match)):
            return f"{evaluate.group(1)}/{evaluate.group(2)}/20{evaluate.group(3)}"
        return evaluate



