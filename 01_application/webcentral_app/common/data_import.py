
class DataImport:
    def __init__(self, path_to_data_file):
        """Constructor of the Base-DataImport-class.

        """
        self.path_to_file = path_to_data_file

    def load(self):
        """load csv/excel-file

        """
        
        # if its a excel file, check if 2 sheets are present:


        if self.path_to_file.endswith(".csv"):
            header, data = self.readCSV(pathFile)
        elif self.path_to_file.endswith(".xlsx"):
            header, data = self.readExcel(pathFile)
        else:
            raise CommandError(
                "Invalid file format. Please provide a .csv or .xlsx file.")

    def readExcel(
            self,
            path: str,
        ) -> tuple:
        """This method reads the excel-file, and loads the content into
        the two variables header and data.

        Parameters:
        path:   str

        Returns:
        header: list
            List of headers from the excel-file.
        data:   list
            list, containing the rows from the excel-file.
        """
        df = pd.read_excel(path)
        df = df.fillna("")
        header = list(df.columns)
        data = df.values.tolist()
        return header, data
