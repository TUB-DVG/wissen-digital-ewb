import os

import deepl

from .data_import import DataImport

class Translator(DataImport):
    """

    """
    
    def __init__(self, pathToDataFile):
        """
        
        """
        super().__init__(pathToDataFile)


    def processTranslation(self, header, data, mapping):
        """translate the fields, which are 

        """
        # header, data = self.load()

        # only translate the elements, which are stated in the mapping-dict:
        dataTranslated = []
        for row in data:
            dataTranslated.append(self._translate(header, row, mapping))


    def _writeToExcel(self, filename, headerList, data, mapping):
        """Writes the content back to a .xlsx-file

        """
        englishDict = {}
        germanDict = {}
        for headerIndex, headerElement in enumerate(headerList):
            if headerElement in mapping.keys():
                headerElementInExcel = headerElement.replace("__en", "")
                englishDict[headerElementInExcel] = []
                for row in data:
                    englishDict[headerElementInExcel].append(row[headerIndex])
            else:
                germanDict[headerElement] = []
                for row in data:
                    germanDict[headerElement].append(row[headerIndex])

        germanDf = pd.DataFrame(data=germanDict)
        englishDf = pd.DataFrame(data=englishDict)
            
        with open(filename, "w") a fileHandler:
            germanDf.to_excel(fileHandler, sheet_name="German")
            englishnDf.to_excel(fileHandler, sheet_name="English")


    def _translate(self, header, row, mapping):
        """

        """
        deeplTranslator = deepl.Translator(os.environ["DeeplKey"])

        for key in mapping.keys():
            headerValueEn = key
            headerValue = key.replace("__en", "")
            # get the german text:
            germanText = row[header.index(headerValue)]
            row[header.index(headerValueEn)] = deeplTranslator.translate_text(germanText, target_lang="EN-US")
        
        return row
