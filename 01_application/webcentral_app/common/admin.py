from django.contrib import admin
from django.contrib.sessions.models import Session
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.template.response import TemplateResponse
from django.urls import path

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
# Define a new admin class for the aggregated session elements