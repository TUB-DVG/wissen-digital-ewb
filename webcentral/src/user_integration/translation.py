from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from .models import (
    UserEngagement,
    ProArgument,
    ConArgument,
    Literature,
    ProcedureItem,
)


class UserEngagementTranslationOptions(TranslationOptions):
    fields = (
        "category",
        "categoryShortDescription",
        "subCategoryShortDescription",
        "timeRequired",
        "groupSize",
        "material",
        "goals",
        "goodPracticeExample",
    )


translator.register(UserEngagement, UserEngagementTranslationOptions)


class ProArgumentTranslationOptions(TranslationOptions):
    fields = ("proArgument",)


translator.register(ProArgument, ProArgumentTranslationOptions)


class ConArgumentTranslationOptions(TranslationOptions):
    fields = ("conArgument",)


translator.register(ConArgument, ConArgumentTranslationOptions)

# class LiteratureTranslationOptions(TranslationOptions):
#     fields = ("literature", )
#
# translator.register(Literature, LiteratureTranslationOptions)


class ProcedureTranslationOptions(TranslationOptions):
    fields = ("procedureItem",)


translator.register(ProcedureItem, ProcedureTranslationOptions)
