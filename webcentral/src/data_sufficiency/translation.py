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
        "example1Heading",
        "example2",
        "example2Heading",
    )


translator.register(DataSufficiency, DataSufficiencyTranslationOptions)
