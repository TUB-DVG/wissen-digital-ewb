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


class ClassificationAdmin(TranslationAdmin):
    pass
admin.site.register(Classification, ClassificationAdmin)

class FocusAdmin(TranslationAdmin):
    pass
admin.site.register(Focus, FocusAdmin)

class ApplicationAreaAdmin(TranslationAdmin):
    pass

admin.site.register(ApplicationArea, ApplicationAreaAdmin)

class UsageAdmin(TranslationAdmin):
    pass
admin.site.register(Usage, UsageAdmin)

class TargetGroupAdmin(TranslationAdmin):
    pass
admin.site.register(TargetGroup, TargetGroupAdmin)

admin.site.register(Tools)

class LifeCyclePhaseAdmin(TranslationAdmin):
    pass

admin.site.register(LifeCyclePhase, LifeCyclePhaseAdmin)

class UserInterfaceAdmin(TranslationAdmin):
    pass

admin.site.register(UserInterface, UserInterfaceAdmin)

class AccessibilityAdmin(TranslationAdmin):
    pass

admin.site.register(Accessibility, AccessibilityAdmin)
admin.site.register(Scale)