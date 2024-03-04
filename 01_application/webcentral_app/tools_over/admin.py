from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
    Tools,
    Classification,
    Focus,
    ApplicationArea,
    Usage,
    TargetGroup,
    LifeCyclePhase,
    UserInterface,
    Accessibility,
    Scale,
)

# Register your models here.
admin.site.register(Tools)

class ClassificationAdmin(TranslationAdmin):
    pass
admin.site.register(Classification, ClassificationAdmin)

class FocusAdmin(TranslationAdmin):
    pass
admin.site.register(Focus, FocusAdmin)

# admin.site.register(ApplicationArea)
class ApplicationAreaAdmin(TranslationAdmin):
    pass

admin.site.register(ApplicationArea, ApplicationAreaAdmin)
admin.site.register(Usage)
admin.site.register(TargetGroup)
admin.site.register(LifeCyclePhase)
admin.site.register(UserInterface)
admin.site.register(Accessibility)
admin.site.register(Scale)