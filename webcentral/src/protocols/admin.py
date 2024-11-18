from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Protocol


class ProtocolAdmin(TranslationAdmin):
    pass


admin.site.register(Protocol, ProtocolAdmin)
