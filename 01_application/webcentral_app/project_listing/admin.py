from django.contrib import admin

from .models import * 








# admin.site.Teilprojekt(Tools) not need here, because it is moved to tools_over
class TeilprojektAdmin(admin.ModelAdmin):

    search_fields = ['fkz',]
admin.site.register(Teilprojekt,TeilprojektAdmin)

class EnargusAdmin(admin.ModelAdmin):

    search_fields = ['enargus_id',]
admin.site.register(Enargus,EnargusAdmin)



class PersonAdmin(admin.ModelAdmin):

    search_fields = ['name',]
admin.site.register(Person,PersonAdmin)

class Leistung_sysAdmin(admin.ModelAdmin):

    search_fields = ['leistungsplansystematik_nr',]
admin.site.register(Leistung_sys,Leistung_sysAdmin)



class Ausfuehrende_stelleAdmin(admin.ModelAdmin):

    search_fields = ['name',]
admin.site.register(Ausfuehrende_stelle,Ausfuehrende_stelleAdmin)



class AnschriftAdmin(admin.ModelAdmin):

    search_fields = ['plz',]
admin.site.register(Anschrift,AnschriftAdmin)

class ForschungAdmin(admin.ModelAdmin):

    search_fields = ['bundesministerium','projekttraeger','forschungsprogramm','foerderprogramm',]
admin.site.register(Forschung,ForschungAdmin)




class Modulen_zuordnung_ptjAdmin(admin.ModelAdmin):

    search_fields = ['mod_id',]
admin.site.register(Modulen_zuordnung_ptj,Modulen_zuordnung_ptjAdmin)



class Fragebogen_21Admin(admin.ModelAdmin): 
    search_fields = ['Fragebogen_21',]
admin.site.register(Fragebogen_21,Fragebogen_21Admin)



class ZuwendungsempfaengerAdmin(admin.ModelAdmin):

    search_fields = ['name',]
admin.site.register(Zuwendungsempfaenger,ZuwendungsempfaengerAdmin)
