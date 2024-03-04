from modeltranslation.translator import translator, TranslationOptions
from .models import (
    ApplicationArea,
    Classification,
    Focus,
)

class ApplicationAreaTranslationOptions(TranslationOptions):
    fields = ("applicationArea",)

class ClassificationTranslationOptions(TranslationOptions):
    fields = ("classification",)

class FocusTranslationOptions(TranslationOptions):
    fields = ("focus",)

translator.register(ApplicationArea, ApplicationAreaTranslationOptions)
translator.register(Classification, ClassificationTranslationOptions)
translator.register(Focus, FocusTranslationOptions)

