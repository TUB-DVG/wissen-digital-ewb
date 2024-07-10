from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
    UserEngagement,
    ProcedureItem,
    Literature,
    ProArgument,
    ConArgument,
)

# class UserEngagementAdmin(TranslationAdmin):
#     pass

# class LiteratureAdmin(TranslationAdmin):
#     pass

# class ProcedureItemAdmin(TranslationAdmin):
#     pass

# class ProArgumentAdmin(TranslationAdmin):
#     pass

# class ConArgumentAdmin(TranslationAdmin):
#     pass

# admin.site.register(UserEngagement, UserEngagementAdmin)
# admin.site.register(Literature, LiteratureAdmin)
# admin.site.register(ProcedureItem, ProcedureItemAdmin)
# admin.site.register(ProArgument, ProArgumentAdmin)
# admin.site.register(ConArgument, ConArgumentAdmin)
admin.site.register(UserEngagement)
admin.site.register(Literature)
admin.site.register(ProcedureItem)
admin.site.register(ProArgument)
admin.site.register(ConArgument)
