import importlib

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = "Exports Data as a Excel sheet from specified App"

    def add_arguments(self, parser):
        parser.add_argument("type_of_data", nargs="+", type=str)
        parser.add_argument("filename", nargs="+", type=str)

    def handle(self, *args, **options):
        """ """

        filename = options["filename"][0]

        type_of_data = options["type_of_data"][0]
        data_import_module = self._checkIfInInstalledApps(type_of_data)
        appDataExportObj = data_import_module.DataExport(filename)
        appDataExportObj.exportToXlsx()

    def _checkIfInInstalledApps(self, type_of_data):
        """Check if user given argument `type_of_data` matches
        one of the installed apps. If it does, check if a `data_export`-module
        is present in that app.
        """
        installed_django_apps = settings.INSTALLED_APPS
        app_names = [app.split(".")[0] for app in installed_django_apps]
        if type_of_data in app_names:
            if (
                importlib.util.find_spec(type_of_data + ".data_export")
                is not None
            ):
                return importlib.import_module(type_of_data + ".data_export")
        raise CommandError(
            """specified type_of_data has no corresponding app or has no 
            data_export.py in the app."""
        )
