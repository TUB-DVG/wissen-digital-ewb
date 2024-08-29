from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from .models import (
    DataSufficiency,
)


class DataSufficiencyTranslationOptions(TranslationOptions):
    fields = (
        "strategyCategory",
        "categoryShortDescription",
        "categoryLongDescription",
        "example1",
        "example2",
    )


translator.register(DataSufficiency, DataSufficiencyTranslationOptions)
