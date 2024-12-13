"""Script to configure the django admin panel for the common app.

This module holds 2 classes. The dirst class `AggregatedSessionByDay` is a 
class based view to handle the page visits. It adds a url in the admin panel
were the aggregated page visits can be seen by day.
The second class `DbDifAdmin` creates a finalize action, which finalizes 
DbDiff conflicts.

"""

import importlib
import json

from modeltranslation.admin import TranslationAdmin
from django.contrib import admin
from django.contrib.sessions.models import Session
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.template.response import TemplateResponse
from django.urls import path
from django.core import serializers
from .models import (
    Classification,
    Focus,
    ApplicationArea,
    Usage,
    TargetGroup,
    LifeCyclePhase,
    UserInterface,
    Accessibility,
    Scale,
    AbstractHistory,
    DbDiff,
    License,
)


class AggregatedSessionByDay(admin.ModelAdmin):
    """Class Definition for admin class based view for the aggregated views
    per day.

    """

    def get_urls(self):
        """Add a url siteVisits/ to the admin panel."""
        urls = super().get_urls()
        my_urls = [
            path(
                "siteVisits/",
                self.admin_site.admin_view(self.adminViewAggregatedSessions),
            ),
        ]
        return my_urls + urls

    def adminViewAggregatedSessions(self, request):
        """Aggregate the sessions by day and render the aggregatedVisits.html"""
        dates, visitsPerDate = self.get_queryset(request)
        context = dict(
            self.admin_site.each_context(request),
        )

        context["dates"] = dates
        context["visitsPerDate"] = visitsPerDate
        return TemplateResponse(
            request, "common/aggregatedVisits.html", context
        )

    def get_queryset(self, request):
        """Get the sessions for an expiration date."""
        queryset = super().get_queryset(request)
        queryset = (
            queryset.annotate(date=TruncDate("expire_date"))
            .values("date")
            .annotate(count=Count("session_key"))
            .order_by("-date")
        )
        dates = []
        visitsPerDate = []
        for element in queryset:
            dates.append(element["date"])
            visitsPerDate.append(element["count"])
        return dates, visitsPerDate


admin.site.register(Session, AggregatedSessionByDay)


class DbDiffAdmin(admin.ModelAdmin):
    """Class to modify functionality of admin site for model `DbDiff`"""

    list_display = ["identifier", "executed"]
    ordering = ["executed"]
    actions = ["finalizeChange"]
    list_filter = ["executed", "identifier"]

    @admin.action(description="Finalize selected changes")
    def finalizeChange(self, request, queryset):
        """Parse the `diffStr` and remove the unused object for all
        referenced tables.
        """
        filterForNotExecuted = queryset.filter(executed=False)

        for dbDiff in filterForNotExecuted:
            diffStr = dbDiff.diffStr
            splitByTable = diffStr.split(";;")
            for tableDiffStr in splitByTable[:-1]:
                splitByNewline = tableDiffStr.split("\n")
                tableIdentifier = splitByNewline[0][:-1]
                idName = splitByNewline[1].split(":")[0].replace(" ", "")
                oldId = (
                    splitByNewline[1]
                    .split(":")[1]
                    .replace(" ", "")
                    .split("->")[0]
                )
                pyClass = self._getClassFromStr(tableIdentifier)
                oldObj = pyClass.objects.get(**{idName: int(oldId)})
                if not self._isObjectReferenced(oldObj):
                    oldObj.delete()

            dbDiff.executed = True
            dbDiff.save()

    def _isObjectReferenced(self, obj):
        """Check if the old object is referenced anywhere and shouldnt be
        deleted.
        """
        model = obj.__class__
        for relatedObject in model._meta.related_objects:
            relatedModel = relatedObject.related_model
            fieldName = relatedObject.field.name
            filterKwargs = {fieldName: obj}

            if relatedModel.objects.filter(**filterKwargs).exists():
                return True
        return False

    def _getClassFromStr(self, classStr):
        """Return a python class object from its string representation.
        E.g.

        classStr:   str
            Str representation of a python class.

        Returns:
            class-object

        # Example
        For "<class 'project_listing.models.FurtherFundingInformation'>" the
        class `FurtherFundingInformation` is returned.
        """
        modulePath, className = (
            classStr.strip("<>").split("'")[1].rsplit(".", 1)
        )

        module = importlib.import_module(modulePath)

        return getattr(module, className)


admin.site.register(DbDiff, DbDiffAdmin)
admin.site.register(License)
# Define a new admin class for the aggregated session elements


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

    actions = ["rollbackHistory"]

    @admin.action(description="Rollback selected change")
    def rollbackHistory(self, request, queryset):
        """Rolls back to the state selected by `queryset`"""
        for historyObj in queryset:
            deserializedStringyfiedObj = serializers.deserialize(
                "custom_json", historyObj.stringifiedObj
            )
            rollbackToolState = list(deserializedStringyfiedObj)[0].object
            toolStateInDB = self.modelInstance.objects.filter(
                **{
                    self.attributeName: getattr(
                        rollbackToolState, self.attributeName
                    )
                }
            )[0]
            toolStateInDB._update(rollbackToolState, historyObj)
            historyObj.delete()

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}

        deserializedStringyfiedObj = serializers.deserialize(
            "custom_json",
            self.historyModelInstance.objects.get(
                id=int(object_id)
            ).stringifiedObj,
        )
        oldTool = list(deserializedStringyfiedObj)[0].object

        currentToolState = self.modelInstance.objects.filter(
            **{self.attributeName: getattr(oldTool, self.attributeName)}
        )

        extra_context["oldTool"] = oldTool
        extra_context["rollbackStateStringified"] = json.loads(
            self.historyModelInstance.objects.get(
                id=int(object_id)
            ).stringifiedObj
        )[0]["fields"]
        extra_context["currentStateStringified"] = json.loads(
            serializers.serialize(
                "json", currentToolState, use_natural_foreign_keys=True
            )
        )[0]["fields"]

        extra_context["currentTool"] = self.modelInstance.objects.filter(
            **{self.attributeName: getattr(oldTool, self.attributeName)}
        )[0]
        # breakpoint()
        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )
