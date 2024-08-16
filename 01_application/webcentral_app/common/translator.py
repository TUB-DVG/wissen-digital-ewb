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


    def _writeToExcel(self, filename, header, data):
        """Writes the content back to a .xlsx-file

        """
        with open(filename, "w") a fileHandler:


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
