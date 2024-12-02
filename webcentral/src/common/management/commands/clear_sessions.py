from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session

class Command(BaseCommand):
    help = "Clears all session data from the database."

    def handle(self, *args, **kwargs):
        session_count = Session.objects.count()
        if session_count == 0:
            self.stdout.write("No sessions to clear.")
        else:
            Session.objects.all().delete()
            self.stdout.write(f"Successfully cleared {session_count} sessions.")
