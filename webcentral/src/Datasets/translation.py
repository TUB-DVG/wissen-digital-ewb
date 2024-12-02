from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from .models import (
    Dataset,
)


class DatasetsTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "provider",
        "availability",
        "coverage",
        "furtherInformation",
        "description",
        # "dataSources",
        "resolution",
        "lastUpdate",
        "licenseNotes",
    )


translator.register(
    Dataset,
    DatasetsTranslationOptions,
)
