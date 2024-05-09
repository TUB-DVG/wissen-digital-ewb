from django.contrib import admin
from .models import (
    Component,
    ComponentClass,
    Category,
)

admin.site.register(Component)
admin.site.register(ComponentClass)
admin.site.register(Category)
