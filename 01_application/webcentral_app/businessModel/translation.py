from modeltranslation.translator import (
    translator,
    TranslationOptions,
)
from .models import BusinessModel


class BusinessModelTranslationOptions(TranslationOptions):
    fields = (
        "challenge",
        "shortDescription",
        "property1",
        "property1Text",
        "property2",
        "property2Text",
        "property3",
        "property3Text",
        "property4",
        "property4Text",
        "property5",
        "property5Text",
    )


translator.register(BusinessModel, BusinessModelTranslationOptions)
