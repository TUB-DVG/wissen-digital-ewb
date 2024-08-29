from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from .models import (
    Category,
    ComponentClass,
    Component,
)


class ComponentClassTranslationOptions(TranslationOptions):
    fields = ("componentClass",)


class CategoryTranslationOptions(TranslationOptions):
    fields = ("category",)


class ComponentTranslationOptions(TranslationOptions):
    fields = (
        "description",
        "furtherInformationNotes",
        "sources",
    )


translator.register(ComponentClass, ComponentClassTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Component, ComponentTranslationOptions)
