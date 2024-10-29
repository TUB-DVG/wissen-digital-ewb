from django.contrib import admin
from django.core import serializers
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
    History,
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


class ToolsAdmin(TranslationAdmin):
    # class Media:
    #     js = (
    #         'modeltranslation/js/force_jquery.js',
    #         'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.24/jquery-ui.min.js',
    #         'modeltranslation/js/tabbed_translation_fields.js',
    #     )
    #     css = {
    #         'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
    #     }
    pass


admin.site.register(Tools, ToolsAdmin)


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


class HistoryAdmin(admin.ModelAdmin):
    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}

        deserializedStringyfiedObj = serializers.deserialize(
            "json", self.model.objects.get(id=int(object_id)).stringifiedObj
        )
        oldTool = list(deserializedStringyfiedObj)[0].object
        extra_context["oldTool"] = oldTool
        extra_context["currentTool"] = Tools.objects.filter(name=oldTool.name)[
            0
        ]
        # breakpoint()
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )


admin.site.register(History, HistoryAdmin)
