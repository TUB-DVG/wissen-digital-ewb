from modeltranslation.admin import TranslationAdmin
from django.contrib import admin

from .models import (
    BusinessModel,
    History,
)
from common.admin import HistoryAdmin


class HistoryAdminApp(HistoryAdmin):
    """ """

    modelInstance = BusinessModel
    historyModelInstance = History
    attributeName = "challenge"


admin.site.register(History, HistoryAdminApp)


class BusinessModelAdmin(TranslationAdmin):
    pass


admin.site.register(BusinessModel, BusinessModelAdmin)
