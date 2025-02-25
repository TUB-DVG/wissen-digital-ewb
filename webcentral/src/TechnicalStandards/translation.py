from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from .models import (
    Norm,
)


class NormTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "name",
        "description",
        "provider",
        "furtherInformation",
        "alternatives",
        "yearOfRelease",
    )


# class ProtocolTranslationOptions(TranslationOptions):
#     fields = (
#         "communicationMediumCategory",
#         "supportedTransmissionMediuems",
#         "openSourceStatus",
#         "licensingFeeRequirement",
#         "networkTopology",
#         "security",
#         "bandwidth",
#         "frequency",
#         "range",
#         "multiMaster",
#         "discovery",
#         "priorities",
#         "osiLayers",
#         "buildingAutomationLayer",
#     )


translator.register(Norm, NormTranslationOptions)
# translator.register(Protocol, ProtocolTranslationOptions)
