from modeltranslation.translator import (
    translator,
    TranslationOptions,
)
from .models import (
    License,
    Accessibility, 
    ApplicationArea,
    Classification,
    Focus,
    Usage,
    Scale,
    LifeCyclePhase,
    TargetGroup,
    UserInterface,
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



class LicenseTranslationOptions(TranslationOptions):
    fields = (
        "license",
        "openSourceStatus",
        "licensingFeeRequirement",
    )

class LifeCyclePhaseTranslationOptions(TranslationOptions):
    fields = ("lifeCyclePhase",)


class UserInterfaceTranslationOptions(TranslationOptions):
    fields = ("userInterface",)


class AccessibilityTranslationOptions(TranslationOptions):
    fields = ("accessibility",)


class ScaleTranslationOptions(TranslationOptions):
    fields = ("scale",)


translator.register(Accessibility, AccessibilityTranslationOptions)
translator.register(ApplicationArea, ApplicationAreaTranslationOptions)
translator.register(Classification, ClassificationTranslationOptions)
translator.register(Focus, FocusTranslationOptions)
translator.register(Usage, UsageTranslationOptions)
translator.register(Scale, ScaleTranslationOptions)
translator.register(TargetGroup, TargetGroupTranslationOptions)
translator.register(LifeCyclePhase, LifeCyclePhaseTranslationOptions)
translator.register(UserInterface, UserInterfaceTranslationOptions)
translator.register(
    License,
    LicenseTranslationOptions,
)
