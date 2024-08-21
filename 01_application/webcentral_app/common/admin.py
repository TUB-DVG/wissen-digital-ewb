import importlib

from django.contrib import admin
from django.contrib.sessions.models import Session
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.template.response import TemplateResponse
from django.urls import path

from .models import DbDiff
# Register your models here.

class AggregatedSessionByDay(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('siteVisits/', self.admin_site.admin_view(self.adminViewAggregatedSessions)),
        ]
        return my_urls + urls
    def adminViewAggregatedSessions(self, request):
        dates, visitsPerDate = self.get_queryset(request)
        context = dict(
            self.admin_site.each_context(request),
        )

        context["dates"] = dates
        context["visitsPerDate"] = visitsPerDate
        return TemplateResponse(request, "common/aggregatedVisits.html", context)
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(date=TruncDate('expire_date')).values('date').annotate(count=Count('session_key')).order_by('-date')
        dates = []
        visitsPerDate = []
        for element in queryset:
            dates.append(element["date"])
            visitsPerDate.append(element["count"])
        return dates, visitsPerDate

    # def changelist_view(self, request, extra_context=None):
    #     response = super().changelist_view(request, extra_context=extra_context)
    #     response.context_data['title'] = 'Aggregated Sessions by Day'
    #     return response

admin.site.register(Session, AggregatedSessionByDay)

class DbDiffAdmin(admin.ModelAdmin):
    """Class to modify functionality of admin site for model `DbDiff`

    """
    list_display = ["identifier", "executed"]
    ordering = ["executed"]
    actions = ["finalizeChange"] 
    list_filter = ["executed", "identifier"]
    
    @admin.action(description="Finalize selected changes")
    def finalizeChange(self, request, queryset):
        """Parse the `diffStr` and remove the unused object for all referenced tables.

        """
        filterForNotExecuted = queryset.filter(executed=False)
        
        for dbDiff in filterForNotExecuted:
            diffStr = dbDiff.diffStr
            splitByTable = diffStr.split(";;")
            for tableDiffStr in splitByTable[:-1]:
                splitByNewline = tableDiffStr.split("\n")
                tableIdentifier = splitByNewline[0][:-1]
                diffAttributes = splitByTable[1:]
                try:
                    idName = splitByNewline[1].split(":")[0].replace(" ", "") 
                except:
                    breakpoint()
                oldId = splitByNewline[1].split(":")[1].replace(" ", "").split("->")[0]
                pyClass = self._getClassFromStr(tableIdentifier)
                oldObj = pyClass.objects.get(**{idName: int(oldId)}) 
                if not self._isObjectReferenced(oldObj):
                    oldObj.delete()
            
            dbDiff.executed = True
            dbDiff.save()


    def _isObjectReferenced(self, obj):
        """Check if the old object is referenced anywhere and shouldnt be deleted.

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
        For "<class 'project_listing.models.FurtherFundingInformation'>" the class 
        `FurtherFundingInformation` is returned.
        """
        modulePath, className = classStr.strip("<>").split("'")[1].rsplit('.', 1)
    
        module = importlib.import_module(modulePath)
    
        return getattr(module, className)
    

admin.site.register(DbDiff, DbDiffAdmin)
# Define a new admin class for the aggregated session elements
