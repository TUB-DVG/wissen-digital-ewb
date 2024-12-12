from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import *
from common.admin import HistoryAdmin


class NormAdmin(TranslationAdmin):
    pass


admin.site.register(Norm, NormAdmin)


class HistoryAdminApp(HistoryAdmin):
    """ """

    modelInstance = Norm
    historyModelInstance = History
    attributeName = "name"


admin.site.register(History, HistoryAdminApp)
