import os


from django import setup
from sys import path as sys_path

sys_path.append("/src/01_application/webcentral_app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webcentral_app.settings")
setup()

from django.contrib.auth.models import User

if not User.objects.filter(
    username=os.environ.get("DJANGO_SUPERUSER_USERNAME")
).exists():
    User.objects.create_superuser(
        os.environ.get("DJANGO_SUPERUSER_USERNAME"),
        os.environ.get("DJANGO_SUPERUSER_EMAIL"),
        os.environ.get("DJANGO_SUPERUSER_PASSWORD"),
    )
