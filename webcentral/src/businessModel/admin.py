from modeltranslation.admin import TranslationAdmin
from django.contrib import admin

from .models import (
    BusinessModel,
)


class BusinessModelAdmin(TranslationAdmin):
    pass


admin.site.register(BusinessModel, BusinessModelAdmin)
