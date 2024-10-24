from modeltranslation.admin import TranslationAdmin
from django.contrib import admin

from .models import (
    Component,
    ComponentClass,
    Category,
)


class ComponentModelAdmin(TranslationAdmin):
    pass


class ComponentClassModelAdmin(TranslationAdmin):
    pass


class CategoryModelAdmin(TranslationAdmin):
    pass


admin.site.register(Component, ComponentModelAdmin)
admin.site.register(ComponentClass, ComponentClassModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
