from django.contrib import admin

from .models import (
    Topic,
    UseCase,
)

admin.site.register(Topic)
admin.site.register(UseCase)