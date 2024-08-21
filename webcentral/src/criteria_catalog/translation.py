from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from .models import (
    CriteriaCatalog,
    Topic,
    Tag,
)


class TopicTranslationOptions(TranslationOptions):
    fields = ("heading", "text")


class TagTranslationOptions(TranslationOptions):
    fields = ("name", )

class CriteriaCatalogTranslationOptions(TranslationOptions):
    fields = ("name", "text")


translator.register(Topic, TopicTranslationOptions)
translator.register(Tag, TagTranslationOptions)
translator.register(CriteriaCatalog, CriteriaCatalogTranslationOptions)
