from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Exports Data as a Excel sheet from specified App"

    def add_arguments(self, parser):
        parser.add_argument("type_of_data", nargs="+", type=str)
        parser.add_argument("filename", nargs="+", type=str)

    def handle(self, *args, **options):
        """

        """
        
        filename = options["filename"][0]

        type_of_data = options["type_of_data"][0]
        data_import_module = self._checkIfInInstalledApps(type_of_data)
        appDataExportObj = data_import_module.DataExport(filename)
        appDataExportObj.exportToXlsx()

