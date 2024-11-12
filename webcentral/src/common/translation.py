from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from .models import (
    License,
)


class LicenseTranslationOptions(TranslationOptions):
    fields = (
        "license",
    )


translator.register(
    License,
    LicenseTranslationOptions,
)
