from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from protocols.models import (
    Protocol,
)


class ProtocolTranslationOptions(TranslationOptions):
    fields = (
        "description",
        # "userInterfaceNotes",
        # "lastUpdate",
        # "licenseNotes",
        "furtherInformation",
        "provider",
        "yearOfRelease",
        "alternatives",
        "communicationMediumCategory",
        "supportedTransmissionMediuems",
        # "openSourceStatus",
        # "licensingFeeRequirement",
        "networkTopology",
        "security",
        "bandwidth",
        "frequency",
        "range",
        "multiMaster",
        "discovery",
        "priorities",
        "osiLayers",
        "buildingAutomationLayer",
    )


translator.register(Protocol, ProtocolTranslationOptions)
