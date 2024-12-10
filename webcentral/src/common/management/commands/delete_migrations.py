import os

from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = "Clears all session data from the database."

              
    def handle(self, *args, **kwargs):
        """

        """
        currentDir = ob.getCwd()
         
        breakpoint() 
