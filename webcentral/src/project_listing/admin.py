"""Configuration of django admin panel for the `prject_listing`-app.

"""

from django.contrib import admin

from .models import (
    Address,
    Enargus,
    ExecutingEntity,
    FurtherFundingInformation,
    GrantRecipient,
    RAndDPlanningCategory,
    Subproject,
    Person,
    ModuleAssignment,
)

admin.site.register(FurtherFundingInformation)
admin.site.register(RAndDPlanningCategory)
admin.site.register(ModuleAssignment)
admin.site.register(ExecutingEntity)
admin.site.register(GrantRecipient)
admin.site.register(Subproject)
admin.site.register(Address)
admin.site.register(Enargus)
admin.site.register(Person)
