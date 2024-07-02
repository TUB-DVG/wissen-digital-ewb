from django.contrib import admin

from .models import (
    UserEngagement,
    ProcedureItem,
    Literature,
)

admin.site.register(UserEngagement)
admin.site.register(Literature)
admin.site.register(ProcedureItem)
