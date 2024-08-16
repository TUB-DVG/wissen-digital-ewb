from django.contrib import admin

from .models import (
    CriteriaCatalog,
    Topic,
    Tag,
)

admin.site.register(Tag)
admin.site.register(Topic)
admin.site.register(CriteriaCatalog)