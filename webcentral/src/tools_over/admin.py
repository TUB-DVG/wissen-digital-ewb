import json

from django.contrib import admin
from django.forms import ModelForm

from modeltranslation.admin import TranslationAdmin

from project_listing.models import Subproject

from common.admin import HistoryAdmin
from .models import Tools, History


class ToolsAdmin(TranslationAdmin):
    pass


admin.site.register(Tools, ToolsAdmin)


class HistoryAdminApp(HistoryAdmin):
    """ """

    modelInstance = Tools
    historyModelInstance = History
    attributeName = "name"


admin.site.register(History, HistoryAdminApp)
