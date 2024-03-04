from django.contrib import admin

from .models import (
    CriteriaCatalog,
    Topic,
)

admin.site.register(Topic)
admin.site.register(CriteriaCatalog)