from django.contrib import admin

from .models import * 

admin.site.register(Teilprojekt)
admin.site.register(Enargus)
admin.site.register(Forschung)
admin.site.register(Fragebogen_21)

admin.site.register(Modulen_zuordnung_ptj)
admin.site.register(Leistung_sys)
admin.site.register(Zuwendungsempfaenger)
admin.site.register(Ausfuehrende_stelle)

admin.site.register(Person)
admin.site.register(Anschrift)

# admin.site.register(Tools) not need here, because it is moved to tools_over
