from django.contrib import admin
from django.core import serializers

from .models import Dataset, History
from common.admin import HistoryAdmin

admin.site.register(Dataset)


class HistoryAdminApp(HistoryAdmin):
    modelInstance = Dataset
    historyModelInstance = History
    attributeName = "name"


admin.site.register(History, HistoryAdminApp)
