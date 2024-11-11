from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from .models import (
    collectedDatasets,
)


class collectedDatasetsTranslationOptions(TranslationOptions):
    fields = (
        "name",
        "applicationArea",
        "categoryDataset",
        "reference",
        "availability",
        "coverage",
        "includesNonResidential",
        "shortDescriptionDe",
        "comment",
        "dataSources",
        "resolution",
    )


translator.register(
    collectedDatasets,
    collectedDatasetsTranslationOptions,
)
