from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from .models import (
    Tools,
)


class ToolsTranslationOptions(TranslationOptions):
    fields = (
        # "name",
        "description",
        "userInterfaceNotes",
        "lastUpdate",
        "licenseNotes",
        "furtherInformation",
        "provider",
        "yearOfRelease",
    )


translator.register(Tools, ToolsTranslationOptions)
