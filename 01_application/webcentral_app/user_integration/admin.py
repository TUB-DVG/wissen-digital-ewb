from django.contrib import admin

from .models import (
    UserEngagement,
    ProcedureItem,
    Literature,
    ProArgument,
    ConArgument,
)

admin.site.register(UserEngagement)
admin.site.register(Literature)
admin.site.register(ProcedureItem)
admin.site.register(ProArgument)
admin.site.register(ConArgument)
