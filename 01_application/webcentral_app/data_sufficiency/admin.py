from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import DataSufficiency


class DataSufficencyAdmin(TranslationAdmin):
    pass


admin.site.register(DataSufficiency, DataSufficencyAdmin)
