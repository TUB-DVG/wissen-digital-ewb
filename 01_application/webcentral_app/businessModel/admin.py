from django.contrib import admin

from .models import (
    BusinessModel,
    UserEngagement,
    SpecificProcedureItem,
    ProcedureItem,
)

admin.site.register(BusinessModel)
admin.site.register(UserEngagement)
admin.site.register(SpecificProcedureItem)
admin.site.register(ProcedureItem)
