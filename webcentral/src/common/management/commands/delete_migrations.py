import os

from django.core.management.base import BaseCommand
from django.apps import apps


class Command(BaseCommand):
    help = "Clears all session data from the database."

    def handle(self, *args, **kwargs):
        """ """
        currentDir = os.getcwd()
        for app in apps.app_configs.values():
            if currentDir in app.path:
                self._removeMigrationFiles(app)

    def _removeMigrationFiles(self, app):
        """Go into app/migrations folder and remove the migration-files."""
        os.chdir(app.path)
        if "migrations" in os.listdir():
            os.chdir("migrations")
            os.system("rm -f 00*")
