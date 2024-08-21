from modeltranslation.translator import (
    translator, 
    TranslationOptions,
)

from .models.publication import (
    Publication,
    Type,
)

class PublicationTranslationOptions(TranslationOptions):
    fields = (
        "title", 
        "journal", 
        "institution", 
        "keywords",
        "abstract",
        "copyright",
    )

class TypeTranslationOptions(TranslationOptions):
    fields = (
        "type", 
        "description", 
        "bibtex_types",
    )

translator.register(Publication, PublicationTranslationOptions)
translator.register(Type, TypeTranslationOptions)