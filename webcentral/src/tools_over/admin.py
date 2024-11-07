from django.contrib import admin
from django.forms import ModelForm

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

# class HistoryForm(ModelForm):
#     model = History
#     def clean(self):
#         return self.cleaned_data
#
class HistoryAdmin(admin.ModelAdmin):
    actions = ["rollbackHistory"]

    @admin.action(description="Rollback selected change")
    def rollbackHistory(self, request, queryset):
        """Rolls back to the state selected by `queryset`

        """
        for historyObj in queryset:
            deserializedStringyfiedObj = serializers.deserialize(
                "json", historyObj.stringifiedObj
            )
            rollbackToolState = list(deserializedStringyfiedObj)[0].object
            toolStateInDB = Tools.objects.filter(name=rollbackToolState.name)[0]
            toolStateInDB._update(rollbackToolState, historyObj)
            historyObj.delete()

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

    # def save_model(self, request, obj, form, change):
    #     """Rollback Tools object to state saved in History object
    #
    #     """
    #     deserializedStringyfiedObj = serializers.deserialize(
    #         "json", self.model.objects.get(id=int(obj)).stringifiedObj
    #     )
    #     rolbackState = list(deserializedStringyfiedObj)[0].object
    #
    #     currentState = Tools.objects.filter(name=oldTool.name)[0]
    #     breakpoint()
    #
    # def response_change(self, request, obj):
    #
    #     breakpoint()
    #
    # def response_add(self, request, obj, post_url_continue=None):
    #     breakpoint()
admin.site.register(History, HistoryAdmin)
