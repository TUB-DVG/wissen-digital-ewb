from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import EnvironmentalImpact


class EnvironmentalImpactAdmin(TranslationAdmin):
    pass


admin.site.register(EnvironmentalImpact, EnvironmentalImpactAdmin)
