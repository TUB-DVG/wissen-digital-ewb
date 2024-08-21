from modeltranslation.translator import (
    translator,
    TranslationOptions,
)

from .models import (
    EnvironmentalImpact, )


class EnvironmentalImpactTranslationOptions(TranslationOptions):
    fields = (
        "category",
        "description",
        "name_digital_application",
        "project_name",
        "partner",
        "consortium",
        "further",
        "digitalApplications",
        "goals",
        "strategies",
        "relevance",
        "problem_statement_and_problem_goals",
       "implementation_in_the_project",
        "evaluation",
    )
translator.register(EnvironmentalImpact, EnvironmentalImpactTranslationOptions)
