from modeltranslation.admin import TranslationAdmin
from django.contrib import admin

from .models import (
    BusinessModel,
    UserEngagement,
    SpecificProcedureItem,
    ProcedureItem,
)


class BusinessModelAdmin(TranslationAdmin):
    pass


admin.site.register(BusinessModel, BusinessModelAdmin)
admin.site.register(UserEngagement)
admin.site.register(SpecificProcedureItem)
admin.site.register(ProcedureItem)
