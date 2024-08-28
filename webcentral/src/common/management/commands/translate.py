"""Command class for the translate django custom admin command

"""
import importlib

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from common.translator import Translator


class Command(BaseCommand):
    """Extend the BaseCommand to create an admin comand `translate`,
    which gets the name of the app, whose data file should be translated,
    the filepasth the the data excel file and a filepath to the target, where
    a new excel file with the translated content should be placed.

    """
    help = "Translate a excel file for a specified app"

    def add_arguments(self, parser):
        parser.add_argument("type_of_data", nargs="+", type=str)
        parser.add_argument("pathFile", nargs="+", type=str)
        parser.add_argument("writeToFile", nargs="+", type=str)

    def handle(self, *args, **options):
        """ Method, which is executed when the translate command is called.
        """
        filePathToData = options["pathFile"][0]
        type_of_data = options["type_of_data"][0]
        writeToFile = options["writeToFile"][0]

        data_import_module = self._checkIfInInstalledApps(type_of_data)

        translator = Translator(filePathToData)
        # instanciate the app-specific data_import class:
        appDataImportObj = data_import_module.DataImportApp(filePathToData)
        header, data = appDataImportObj.load()
        dataTranslated = translator.processTranslation(
            header, data, appDataImportObj.MAPPING_EXCEL_DB_EN
        )
        translator._writeToExcel(
            writeToFile,
            header,
            dataTranslated,
            appDataImportObj.MAPPING_EXCEL_DB_EN,
        )

    def _checkIfInInstalledApps(self, type_of_data):
        """Check if user given argument `type_of_data` matches
        one of the installed apps. If it does, check if a `data_import`-module
        is present in that app.
        """
        installed_django_apps = settings.INSTALLED_APPS
        app_names = [app.split(".")[0] for app in installed_django_apps]
        if type_of_data in app_names:
            if (
                importlib.util.find_spec(type_of_data + ".data_import")
                is not None
            ):
                return importlib.import_module(type_of_data + ".data_import")
        raise CommandError(
            "specified type_of_data has no corresponding app or has no data_import.py in the app."
        )
