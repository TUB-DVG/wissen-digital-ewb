"""Loads different types of Data into the Django-Database.

This module loads different types of Data into the Postgres-Database
via the Django-Application. Therefore it gets a .csv-file, which holds 
the datasets. 
`data_import` allows to load different kind of datasets
into the Database. The data-kind needs to be specified in the filename
of the .csv-file:
`enargus`: Enargus-Data
`modulzuordnung`: Modul-Data
`Tools`: Tools-Data
`schlagwoerter`: Schlagwörter-Data
`weatherdata`: Wheaterdata
If none of these sub-strings is present in the filename, the data can 
not be processed and an error is printed. 
The relational model of the database is composed of multiple tables,
which are connected via foreign-keys. The central table, which connects
the different parts together is the `Subproject`-table. It holds all the
foreign-keys, which point to the Enagus-Table, the 
Schlagwörter_erstichtung-table and so on. If a dataset inside the to be
loaded .csv-file contains a Förderkennzeichen (fkz), which is already 
present in the Subproject-table, but has differences in the other 
columns, an IntegrityError is thrown, because the data cannot be 
connected with the fkz. In this situation, the `compareForeignTables`-
method is called, which wlaks though all tables and builds an 
DatabaseDifference-Object, which holds the differences between
the currentState (dataset, which is currently connected to the 
fkz inside the database.) and the pendingState (dataset, which can 
not connected to the fkz, because the currentState is already 
connected to it.). 
At the moment, all DatabaseDifference-Objects are serialized
and written to a.YAML-File. The .yaml-file is named as the current
timestamp.
The `data_import`-Script can be started as a Django-Command. For
that, the current directory needs to be changed to the folder
containing the Django `manage.py`. From there, the following
command needs to be run:
```
    python3 manage.py data_import enargus_01.csv
```
This command loads the enargus_01.csv into the database. For
eventually upcoming Conflicts, a .yaml-file is created. 
The .yaml-file can then be modified to decide, if the currentState
should be kept while the pendingState is deleted, or 
the pendingState should be kept and the currentState should be
deleted. The modified file can then be used as an input for the
`execute_db_changes` command.
"""

import importlib

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


from keywords.models import (
    Keyword,
    KeywordRegisterFirstReview,
)
from weatherdata_over.models import Weatherdata


class MultipleFKZDatasets(Exception):
    """Custom Exception, which is thrown when multiple changes for one
    Förderkennzeichen are written to .yaml-file.
    """


class Command(BaseCommand):
    """This class acts as a Django-Admin command. It can be executed with
    the manage.py by specifing the name of the modul (at the moment
    `data_import`). Furthermore a parameter needs to be present, which is
    the relative-path to a .csv-file, which holds datasets, which should
    be imported into the database.
    An execution could look like this:
    ```
        python3 manage.py data_import
        ../../02_work_doc/01_daten/01_prePro/enargus_csv_20230403.csv
    ```
    At the moment, the .csv-files need to be named acording to the data.
    it holds. (TODO: This has to be changed)

    enargus-data needs to have "enargus" in its filename.
    modulzurodnung-data needs to have "modul" in its filename.
    wheaterdata needs to have "wheaterdata" in its filename.
    schlagwoerter-data needs to have "schlagwoerter" in its filename.
    """

    def __init__(self) -> None:
        """Constructor of `data_import`-command

        This method serves as constructor for the Command-Class.
        It is used to create the Filename of the .YAML-File,
        which is a timestamp of the current datetime. Furthermore
        fkzWrittenToYAML is initialized as empty list,
        in which later every Förderkennzeichen(fkz) is saved,
        which produced an conflict with a dataset inside the database.

        Returns:
        None
        """
        super().__init__()
        self.fkzWrittenToYAML = []

    def getOrCreateWeatherdata(
        self,
        row: list,
        header: list,
    ) -> tuple:
        """Gets or Creates an object of type Weatherdata from row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        Weatherdata according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    Weatherdata
            Weatherdata-object, represent the created or in database
            present Weatherdata-Dataset with the data from row.
        created:    bool
            Indicates, if the Weatherdata-object was created or not.
        """

        dataService = row[header.index("data_service")]
        shortDescription = row[header.index("short_description")]
        provider = row[header.index("provider")]
        furtherInfos = row[header.index("further_information")]
        dataUrl = row[header.index("data_url")]
        logoUrl = row[header.index("logo_url")]
        applications = row[header.index("applications")]
        lastUpdate = row[header.index("last_update")]
        licenseStr = row[header.index("license")]
        category = row[header.index("category")]
        longDescription = row[header.index("long_description")]

        obj, created = Weatherdata.objects.get_or_create(
            data_service=dataService,
            short_description=shortDescription,
            provider=provider,
            further_information=furtherInfos,
            data_url=dataUrl,
            logo_url=logoUrl,
            applications=applications,
            last_update=lastUpdate,
            license=licenseStr,
            category=category,
            long_description=longDescription,
        )
        return obj, created

    # def getOrCreatePublications(self, row, header):
    #     """
    #     Add entry (Publications) into the table or/and return entry key.
    #     """
    #     type_ = row[header.index("type")]
    #     title = row[header.index("title")]
    #     copyright = row[header.index("copyright")]
    #     url = row[header.index("url")]
    #     abstract = row[header.index("abstract")]
    #     institution = row[header.index("institution")]
    #     authors = row[header.index("authors")]
    #     month = row[header.index("month")]
    #     year = row[header.index("year")]
    #     doi = row[header.index("doi")]
    #     keywords = row[header.index("keywords")]
    #     focus = row[header.index("focus")]
    #     journal = row[header.index("journal")]
    #     volume = row[header.index("volume")]
    #     number = row[header.index("number")]
    #     pages = row[header.index("pages")]
    #     pdf = row[header.index("pdf")]
    #     image = row[header.index("image")]
    #
    #     focusList = row[header.index("focus")].split(",")
    #     processedFocusList = self._correctReadInValue(
    #         row[header.index("focus")]
    #     )
    #     focusList = self._iterateThroughListOfStrings(processedFocusList,
    # Focus)
    #     focusElements = Focus.objects.filter(focus__in=focusList)
    #
    #     typeORMObjList = Type.objects.filter(type=type_)
    #     if len(typeORMObjList) == 0:
    #         Type.objects.create(type=type_)
    #
    #     typeORMObj = Type.objects.filter(type=type_)[0]
    #
    #     if number == "":
    #         number = None
    #
    #     if volume == "":
    #         volume = None
    #
    #     if month == "":
    #         month = None
    #     else:
    #         month = int(month)
    #
    #     if year == "":
    #         year = None
    #     else:
    #         year = int(year)
    #
    #     obj, created = Publication.objects.get_or_create(
    #         type=typeORMObj,
    #         title=title,
    #         copyright=copyright,
    #         url=url,
    #         abstract=abstract,
    #         institution=institution,
    #         authors=authors,
    #         month=month,
    #         year=year,
    #         doi=doi,
    #         keywords=keywords,
    #         journal=journal,
    #         volume=volume,
    #         number=number,
    #         pages=pages,
    #         pdf=pdf,
    #         image=image,
    #     )
    #     obj.focus.add(*focusElements)
    #     return obj, created
    #
    def getOrCreateKeyword(
        self,
        row: list,
        header: list,
        catchphraseKey: str,
    ) -> tuple:
        """Gets or Creates an object of type Keyword from row

        This method feeds the data present in row into the django
        get_or_create-function, which returns an Object of Type
        Keyword according to the fed-data. Either this object
        corresponds to a new created-dataset in the database or
        the existing dataset is returned.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    Keyword
            Keyword-object, represent the created or in database
            present Keyword-Dataset with the data from row.
        created:    bool
            Indicates, if the Keyword-object was created or not.
        """
        # content = row[number of the columns of the row]
        keywordFromCSV = row[header.index(catchphraseKey)]
        obj, created = Keyword.objects.get_or_create(
            keyword=keywordFromCSV,
        )
        return obj, created

    def getOrCreateKeywordRegisterFirstReview(
        self,
        row: list,
        header: list,
    ) -> tuple:
        """Gets or Creates KeywordRegisterFirstReview from Row

        This method feeds the data present in row into
        `getOrCreateKeyword`, which returns either an object
        which corresponds to a newly created Dataset inside the
        Database or to an already existed Keyword. The returned
        Keyword-objects are then used to get or create a
        KeywordRegisterFirstReview-object.

        Parameters:
        row:    list
            A dataset, represented by a list.
        header: list
            list of strings, which represent the header-columns.

        Returns:
        obj:    KeywordRegisterFirstReview
            KeywordRegisterFirstReview-object, represent
            the created or in database present Keyword-Dataset
            with the data from row.
        created:    bool
            Indicates, if the KeywordRegisterFirstReview-object
            was created or not.
        """

        objKeyword1, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort1",
        )
        objKeyword2, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort2",
        )
        objKeyword3, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort3",
        )
        objKeyword4, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort4",
        )
        objKeyword5, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort5",
        )
        objKeyword6, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort6",
        )
        objKeyword7, _ = self.getOrCreateKeyword(
            row,
            header,
            "Schlagwort",
        )

        obj, created = KeywordRegisterFirstReview.objects.get_or_create(
            keyword1=objKeyword1,
            keyword2=objKeyword2,
            keyword3=objKeyword3,
            keyword4=objKeyword4,
            keyword5=objKeyword5,
            keyword6=objKeyword6,
            keyword7=objKeyword7,
        )
        return obj, created

    def _checkIfInInstalledApps(self, type_of_data):
        """Check if user given argument `type_of_data` matches
        one of the installed apps. If it does, check if a `data_import`-module
        is present in that app.
        """
        installed_django_apps = settings.INSTALLED_APPS
        app_names = [app.split(".")[0] for app in installed_django_apps]
        if type_of_data in app_names:
            if importlib.util.find_spec(type_of_data + ".data_import") is not None:
                return importlib.import_module(type_of_data + ".data_import")
        raise CommandError(
            """specified type_of_data has no corresponding app or has no 
            data_import.py in the app."""
        )

    def handle(
        self,
        *args: tuple,
        **options: dict,
    ) -> None:
        """This method is called from the manage.py when the 'data_import'
        command is called together with the manage.py.

        Parameters:
        *args:  tuple
            Tuple of arguments, which get unpacked.
        **options:  dict
            Dictionary, contains the parsed argument, given at the CLI
            when calling `python manage.py data_import`

        Returns:
        None
        """
        filePathToData = options["pathCSV"][0]

        type_of_data = options["type_of_data"][0]
        data_import_module = self._checkIfInInstalledApps(type_of_data)

        # else:
        #     raise CommandError(
        #         "Invalid file format. Please provide a .csv or .xlsx file.")
        # pathStr, filename = os.path.split(filePathToData)
        # self.filename = filename
        # self.targetFolder = options["targetFolder"][0]

        appDataImportObj = data_import_module.DataImportApp(filePathToData)
        header, data = appDataImportObj.load()
        appDataImportObj.importList(header, data)

    def add_arguments(
        self,
        parser,
    ) -> None:
        """This method parses the arguments, which where given when
        calling the data_import-command together with the manage.py.
        The Arguments are then given to the handle-method, and can
        be accessed as python-variables.

        Parameters:
        parser: django.parser
        Django parser object, which handles the parsing of the command
        and arguments.

        Returns:
        None
        """
        parser.add_argument("type_of_data", nargs="+", type=str)

        parser.add_argument("pathCSV", nargs="+", type=str)
        # parser.add_argument("targetFolder", nargs="+", type=str)
