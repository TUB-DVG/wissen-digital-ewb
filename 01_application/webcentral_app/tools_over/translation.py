from modeltranslation.translator import translator, TranslationOptions
from .models import (
    ApplicationArea,
    Classification,
    Focus,
    Usage,
    TargetGroup,
)

class ApplicationAreaTranslationOptions(TranslationOptions):
    fields = ("applicationArea",)

class ClassificationTranslationOptions(TranslationOptions):
    fields = ("classification",)

class FocusTranslationOptions(TranslationOptions):
    fields = ("focus",)

class UsageTranslationOptions(TranslationOptions):
    fields = ("usage",)

class TargetGroupTranslationOptions(TranslationOptions):
    fields = ("targetGroup",)

translator.register(ApplicationArea, ApplicationAreaTranslationOptions)
translator.register(Classification, ClassificationTranslationOptions)
translator.register(Focus, FocusTranslationOptions)
translator.register(Usage, UsageTranslationOptions)
translator.register(TargetGroup, TargetGroupTranslationOptions)

