from modeltranslation.translator import (
    translator, 
    TranslationOptions,
)

from .models import UseCase

class UseCaseTranslationOptions(TranslationOptions):
    fields = (
        "useCase",
        "sriLevel",
        "levelOfAction",
        "degreeOfDetail",
        "idPerspectiveforDetail",
        "effectEvaluation",
        "effectName",
        "effectDescription",
        "furtherInformation",
    )

translator.register(UseCase, UseCaseTranslationOptions)
