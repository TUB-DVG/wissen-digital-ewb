from modeltranslation.translator import (
    translator, 
    TranslationOptions,
)

from .models import (
    Weatherdata,
)

class WeatherdataTranslationOptions(TranslationOptions):
    fields = (
        "data_service", 
        "short_description", 
        "provider", 
        "further_information",
        "applications",
        "last_update",
        "license",
        "category",
        "long_description",
    )


translator.register(
    Weatherdata,
    WeatherdataTranslationOptions,
)