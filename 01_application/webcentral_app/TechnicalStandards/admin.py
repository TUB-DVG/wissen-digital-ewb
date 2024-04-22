from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import *

class NormAdmin(TranslationAdmin):
    pass
admin.site.register(Norm, NormAdmin)

class ProtocolAdmin(TranslationAdmin):
    pass
admin.site.register(Protocol, ProtocolAdmin)
