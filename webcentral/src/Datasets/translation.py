from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from .models import (
    Dataset,
)


class collectedDatasetsTranslationOptions(TranslationOptions):
    fields = (
        "name",
        # "applicationArea",
        # "categoryDataset",
        "provider",
        "availability",
        "coverage",
        "furtherInformation",
        "shortDescriptionDe",
        # "comment",
        "dataSources",
        "resolution",
        "lastUpdate",
        "licenseNotes",
    )


translator.register(
    collectedDatasets,
    collectedDatasetsTranslationOptions,
)
