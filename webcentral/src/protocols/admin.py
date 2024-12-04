from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Protocol, History
from common.admin import HistoryAdmin


class ProtocolAdmin(TranslationAdmin):
    pass


admin.site.register(Protocol, ProtocolAdmin)


class HistoryAdminApp(HistoryAdmin):
    """ """

    modelInstance = Protocol
    historyModelInstance = History


admin.site.register(History, HistoryAdminApp)
