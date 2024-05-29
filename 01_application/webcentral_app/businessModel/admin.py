from django.contrib import admin

from .models import (
    BusinessModel,
    UserEngagement,
)

admin.site.register(BusinessModel)
admin.site.register(UserEngagement)
