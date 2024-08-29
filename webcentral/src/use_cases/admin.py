from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

# Register your models here.
from .models import UseCase


class UseCaseAdmin(TranslationAdmin):
    pass


admin.site.register(UseCase, UseCaseAdmin)
