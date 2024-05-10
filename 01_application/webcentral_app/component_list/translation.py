from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from .models import (
    Category,
    ComponentClass,
)


class ComponentClassTranslationOptions(TranslationOptions):
    fields = ("componentClass", )


class CategoryTranslationOptions(TranslationOptions):
    fields = ("category", )


translator.register(ComponentClass, ComponentClassTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
