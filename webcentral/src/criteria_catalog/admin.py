from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
    CriteriaCatalog,
    Topic,
    Tag,
)


class TagModelAdmin(TranslationAdmin):
    pass


class TopicModelAdmin(TranslationAdmin):
    pass


class CriteriaCatalogAdmin(TranslationAdmin):
    pass


admin.site.register(Tag, TagModelAdmin)
admin.site.register(Topic, TopicModelAdmin)
admin.site.register(CriteriaCatalog, CriteriaCatalogAdmin)
