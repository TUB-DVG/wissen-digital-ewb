from django.contrib import admin
from django.core import serializers

from .models import Dataset, HistoryDataset

admin.site.register(Dataset)


class HistoryAdmin(admin.ModelAdmin):
    actions = ["rollbackHistory"]

    @admin.action(description="Rollback selected change")
    def rollbackHistory(self, request, queryset):
        """Rolls back to the state selected by `queryset`"""
        for historyObj in queryset:
            deserializedStringyfiedObj = serializers.deserialize(
                "json", historyObj.stringifiedObj
            )
            rollbackToolState = list(deserializedStringyfiedObj)[0].object
            toolStateInDB = Dataset.objects.filter(name=rollbackToolState.name)[
                0
            ]
            toolStateInDB._update(rollbackToolState, historyObj)
            historyObj.delete()

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}

        deserializedStringyfiedObj = serializers.deserialize(
            "json", self.model.objects.get(id=int(object_id)).stringifiedObj
        )
        oldTool = list(deserializedStringyfiedObj)[0].object

        currentToolState = Dataset.objects.filter(name=oldTool.name)

        extra_context["oldTool"] = oldTool
        extra_context["rollbackStateStringified"] = json.loads(
            self.model.objects.get(id=int(object_id)).stringifiedObj
        )[0]["fields"]
        extra_context["currentStateStringified"] = json.loads(
            serializers.serialize(
                "json", currentToolState, use_natural_foreign_keys=True
            )
        )[0]["fields"]

        extra_context["currentTool"] = Dataset.objects.filter(
            name=oldTool.name
        )[0]
        # breakpoint()
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )


admin.site.register(HistoryDataset, HistoryAdmin)
