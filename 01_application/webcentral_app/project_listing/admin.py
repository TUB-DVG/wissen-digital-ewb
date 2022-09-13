from django.contrib import admin

from import_export import fields,resources
from import_export.widgets import *
from import_export.admin import ImportExportModelAdmin , ImportMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template.response import TemplateResponse
from .models import * 
from django.shortcuts import redirect
from django.utils.translation import gettext as _
#chars = ascii_lowercase + digits

#lst = [''.join(choice(chars) for _ in range(2)) for _ in range(100)]

admin.site.register(Forschung)
admin.site.register(Fragebogen_21)
admin.site.register(Modulen_zuordnung_ptj)  
admin.site.register(Zuwendungsempfaenger)
admin.site.register(Ausfuehrende_stelle)
admin.site.register(Person)
admin.site.register(Anschrift)


admin.site.register(Enargus)

class TeilProjektResource(resources.ModelResource,ImportMixin):
    
    #widget=ForeignKeyWidget(Enargus,'enargus_id')
   
    
    datenbank=fields.Field(
        attribute='enargus_daten__datenbank',
        column_name='Datenbank',
        widget=CharWidget()  
    )
        
      
    thema=fields.Field(
        attribute='enargus_daten__thema',
        column_name='Thema',
        widget=CharWidget()
        
    )

    verbundbezeichnung=fields.Field(
        attribute='enargus_daten__verbundbezeichnung',
        column_name='Verbundbezeichung',
        widget=CharWidget()
    
        
    )  
    
    beschreibung_de=fields.Field(
        attribute='enargus_daten__kurzbeschreibung_de',
        column_name='Kurzbeschreibung_de',
        widget=CharWidget()
    
        
    )
    beschreibung_en=fields.Field(
        attribute='enargus_daten__kurzbeschreibung_en',
        column_name='Kurzbeschreibung_en',
        widget=CharWidget()
    
        
    )
    projektleiter_name=fields.Field(
        attribute='enargus_daten__projektleiter__name',
        column_name='Name_pl',
        widget=CharWidget()   
    )
    projektleiter_vname=fields.Field(
        attribute='enargus_daten__projektleiter__vorname',
        column_name='Vorname_pl',
        widget=CharWidget()   
    )
    projektleiter_email=fields.Field(
        attribute='enargus_daten__projektleiter__email',
        column_name='Email_pl',
        widget=CharWidget()   
    )
    projektleiter_titel=fields.Field(
        attribute='enargus_daten__projektleiter__titel',
        column_name='Titel_pl',
        widget=CharWidget()   
    )

    laufzeitbeginn=fields.Field(
        attribute='enargus_daten__laufzeitbeginn',
        column_name='Laufzeitbeginn', ##
        widget=DateWidget()   
    )
    laufzeitende=fields.Field(
        attribute='enargus_daten__laufzeitende',
        column_name='Laufzeitende',###
        widget=DateWidget()   
    )
    Foerdersumme=fields.Field(
        attribute='enargus_daten__foerdersumme',
        column_name='Foerdersumme_EUR',###
        widget=DecimalWidget()
         
    )
    
    leisstungplan_nr=fields.Field(
        attribute='enargus_daten__leistungsplan_systematik__leistungsplansystematik_nr',
        column_name='Leistungsplan_Sys_Nr',###
        widget=CharWidget()   
    )
    leisstungplan_txt=fields.Field(
        attribute='enargus_daten__leistungsplan_systematik__leistungsplansystematik_text',
        column_name='Leistungsplan_Sys_Text',###
        widget=CharWidget()   
    )
  
    Ausfuehrende_st_name=fields.Field(
        attribute='enargus_daten__ausfuehrende_stelle__name',
        column_name='Name_AS',###
        widget=CharWidget()   
    )
    Ausfuehrende_st_plz=fields.Field(
        attribute='enargus_daten__ausfuehrende_stelle__anschrift__plz',
        column_name='PLZ_AS',###
        widget=CharWidget()   
    )
    Ausfuehrende_st_ort=fields.Field(
        attribute='enargus_daten__ausfuehrende_stelle__anschrift__ort',
        column_name='Ort_AS',###
        widget=CharWidget()   
    )
    Ausfuehrende_st_Adress=fields.Field(
        attribute='enargus_daten__ausfuehrende_stelle__anschrift__adresse',
        column_name='Adress_AS',###
        widget=CharWidget()   
    )
    Ausfuehrende_st_land=fields.Field(
        attribute='enargus_daten__ausfuehrende_stelle__anschrift__land',
        column_name='Land_AS',###
        widget=CharWidget()   
    )
    
    zuwendsempfanger_name=fields.Field(
        attribute='enargus_daten__zuwendsempfanger__name',
        column_name='Name_ZWE',###
        widget=CharWidget()   
    )
    zuwendsempfanger_plz=fields.Field(
        attribute='enargus_daten__zuwendsempfanger__anschrift__plz',
        column_name='PLZ_ZWE',###
        widget=CharWidget()   
    )
    zuwendsempfanger_ort=fields.Field(
        attribute='enargus_daten__zuwendsempfanger__anschrift__ort',
        column_name='Ort_ZWE',###
        widget=CharWidget()   
    )
    zuwendsempfanger_land=fields.Field(
        attribute='enargus_daten__zuwendsempfanger__anschrift__land',
        column_name='Land_ZWE',###
        widget=CharWidget()   
    )
    zuwendsempfanger_address=fields.Field(
        attribute='enargus_daten__zuwendsempfanger__anschrift__adresse',
        column_name='Adress_ZWE',###
        widget=CharWidget()   
    )
    bundesministerium=fields.Field(
        attribute='enargus_daten__forschung__bundesministerium',
        column_name='Bundesministerium',###
        widget=CharWidget()   
    )

    projekttraeger=fields.Field(
        attribute='enargus_daten__forschung__projekttraeger',
        column_name='Projekttraeger',###
        widget=CharWidget()   
    )

    forschungsprogramm=fields.Field(
        attribute='enargus_daten__forschung__forschungsprogramm',
        column_name='Forschungsprogramm',###
        widget=CharWidget()   
    )

    foerderprogramm=fields.Field(
        attribute='enargus_daten__forschung__foerderprogramm',
        column_name='Foerderprogramm',###
        widget=CharWidget()   
    )
    

    
    

    list_attrb=['enargus_daten__datenbank', 'enargus_daten__thema', 'enargus_daten__verbundbezeichnung', 
    'enargus_daten__kurzbeschreibung_de', 'enargus_daten__kurzbeschreibung_en', 'enargus_daten__projektleiter__name', 
    'enargus_daten__projektleiter__vorname', 'enargus_daten__projektleiter__email', 'enargus_daten__projektleiter__titel',
    'enargus_daten__laufzeitbeginn', 'enargus_daten__laufzeitende', 'enargus_daten__foerdersumme','enargus_daten__leistungsplan_systematik__leistungsplansystematik_nr', 
    'enargus_daten__leistungsplan_systematik__leistungsplansystematik_text', 'enargus_daten__ausfuehrende_stelle__name', 'enargus_daten__ausfuehrende_stelle__anschrift__plz', 
    'enargus_daten__ausfuehrende_stelle__anschrift__ort', 'enargus_daten__ausfuehrende_stelle__anschrift__adresse', 'enargus_daten__ausfuehrende_stelle__anschrift__land', 
    'enargus_daten__zuwendsempfanger__name', 'enargus_daten__zuwendsempfanger__anschrift__plz', 'enargus_daten__zuwendsempfanger__anschrift__ort', 'enargus_daten__zuwendsempfanger__anschrift__land', 
    'enargus_daten__zuwendsempfanger__anschrift__adresse', 'enargus_daten__forschung__bundesministerium', 'enargus_daten__forschung__projekttraeger', 'enargus_daten__forschung__forschungsprogramm', 
    'enargus_daten__forschung__foerderprogramm', 'fkz', 'enargus_daten', 'zuordnung', 'schlagwortregister_erstsichtung', 'fragebogen_21']
    
    class Meta:
        model   =   Teilprojekt
        import_id_fields = ['fkz']
        skip_unchanged = True
        report_skipped=False
       

        
    
    #def after_import_instance(self, instance, new, row_number=None, **kwargs):
     #   if new:
    
    def skip_row(self, instance, original):
        """
        Returns ``True`` if ``row`` importing should be skipped.

        Default implementation returns ``False`` unless skip_unchanged == True
        and skip_diff == False.

        If skip_diff is True, then no comparisons can be made because ``original``
        will be None.

        When left unspecified, skip_diff and skip_unchanged both default to ``False``, 
        and rows are never skipped. 

        Override this method to handle skipping rows meeting certain
        conditions.

        Use ``super`` if you want to preserve default handling while overriding
        ::
            class YourResource(ModelResource):
                def skip_row(self, instance, original):
                    # Add code here
                    return super(YourResource, self).skip_row(instance, original)

        """
        if not self._meta.skip_unchanged or self._meta.skip_diff:
            print(true)
            return False
        for field in self.get_import_fields():
            #print(field)
            try:
                # For fields that are models.fields.related.ManyRelatedManager
                # we need to compare the results
                if list(field.get_value(instance).all()) != list(field.get_value(original).all()):
                    print('true')
                    return False
            except AttributeError:
                if ((field.get_value(instance)) != field.get_value(original)) and (field.column_name!='PLZ_AS'):

                #if (field.get_value(instance) != field.get_value(original)) :  
                    if(field.column_name=='Foerdersumme_EUR'):
                        #print(field.get_value(instance))
                        print(field.get_value(original))
                        #print(original)
                        #print(field.__dict__)
                    return False
        return True
        
 
          
    def before_import_row(self, row, row_number=None, **kwargs):
        self.data=row
        set=True
        #print(self.backup['datenbank'].attribute)
        #print(self.backup['datenbank'].attribute)
        #print(type(self.fields))

        if not Teilprojekt.objects.filter(fkz=row['fkz']).exists():
            #for f in self.get_export_order():
             #   i=0
              #  if f !='fkz' :
               #     self.fields[f].attribute=lst[i]
                #    i+=1
            self.fields['laufzeitbeginn'].attribute='ebbbb'
            self.fields['laufzeitende'].attribute='epppp'
            self.fields['zuwendsempfanger_name'].attribute='enarten'
            self.fields['zuwendsempfanger_plz'].attribute='enargusen'
            self.fields['zuwendsempfanger_ort'].attribute='enarguen'
            self.fields['zuwendsempfanger_land'].attribute='enaaten'
            self.fields['zuwendsempfanger_address'].attribute='enargen'
            self.fields['projektleiter_titel'].attribute='enargus_dn'
            self.fields['projektleiter_name'].attribute='enargus_ten'
            self.fields['projektleiter_vname'].attribute='en'
            self.fields['projektleiter_email'].attribute='enars_ten'
            self.fields['Ausfuehrende_st_plz'].attribute='needstochange'
            self.fields['Ausfuehrende_st_land'].attribute='ena'
            self.fields['Ausfuehrende_st_ort'].attribute='enb'
            self.fields['Ausfuehrende_st_name'].attribute='enc'
            self.fields['Ausfuehrende_st_Adress'].attribute='enpppp'
            self.fields['datenbank'].attribute='enmmm'
            self.fields['thema'].attribute='errr'
            self.fields['leisstungplan_nr'].attribute='ennnnnnnnnnn'
            self.fields['leisstungplan_txt'].attribute='ekkkkkkkkkkkkkk'
            self.fields['beschreibung_de'].attribute='else'
            self.fields['beschreibung_en'].attribute='eooooo'
            self.fields['foerderprogramm'].attribute='epooo'
            self.fields['forschungsprogramm'].attribute='whatever'
            self.fields['projekttraeger'].attribute='enargi'
            self.fields['bundesministerium'].attribute='enargo'
            self.fields['verbundbezeichnung'].attribute='enargiii'
            self.fields['Foerdersumme'].attribute='buggy'

            #self.fields['Ausfuehrende_st_address'].attribute='enarg'
            
            set=False
            #print('1')
        else:
            if (not Teilprojekt.objects.get(fkz=row['fkz']).enargus_daten.projektleiter):
                self.fields['projektleiter_titel'].attribute='enargus_dn'
                self.fields['projektleiter_name'].attribute='enargus_ten'
                self.fields['projektleiter_vname'].attribute='en'
                self.fields['projektleiter_email'].attribute='enars_ten'
                set=False

            if (not Teilprojekt.objects.get(fkz=row['fkz']).enargus_daten.zuwendsempfanger):
                self.fields['zuwendsempfanger_name'].attribute='enarten'
                self.fields['zuwendsempfanger_plz'].attribute='enargusen'
                self.fields['zuwendsempfanger_ort'].attribute='enarguen'
                self.fields['zuwendsempfanger_land'].attribute='enaaten'
                self.fields['zuwendsempfanger_address'].attribute='enargen'
                set=False

            if (not Teilprojekt.objects.get(fkz=row['fkz']).enargus_daten.ausfuehrende_stelle):
                self.fields['Ausfuehrende_st_plz'].attribute='noooo'
                self.fields['Ausfuehrende_st_land'].attribute='ena'
                self.fields['Ausfuehrende_st_ort'].attribute='enb'
                self.fields['Ausfuehrende_st_name'].attribute='enc'
                self.fields['Ausfuehrende_st_Adress'].attribute='enpppp'
                set=False

            if (not Teilprojekt.objects.get(fkz=row['fkz']).enargus_daten.leistungsplan_systematik):
                self.fields['leisstungplan_nr'].attribute='ennnnnnnnnnn'
                self.fields['leisstungplan_txt'].attribute='ekkkkkkkkkkkkkk'
                set=False
        
        if set ==True:
            #self.fields['datenbank'].attribute='enargus_daten__datenbank'
            #print(self.get_export_order())
            i=0
            #print(self.list_attrb[i])
            for f in self.get_export_order():
                self.fields[f].attribute=self.list_attrb[i]
                i=i+1
        #print(self.fields['datenbank'].attribute)

        #obj=Teilprojekt.objects.get(fkz=row['fkz'])
        #print(obj.enargus_daten.datenbank)
        #obj.enargus_daten.datenbank=row['db']
        #print (obj.enargus_daten.datenbank)
        #obj.enargus_daten.save(update_fields=['datenbank'])
        #obj2=Teilprojekt.objects.get(fkz=row['fkz'])
        #print (obj2.enargus_daten.datenbank)
    #def after_import_row(self, row, row_result, **kwargs):
     #   self.fields=self.backup
      #  print(self.data)
       # print(self.backup['datenbank'].attribute)

     
    
   

    def after_save_instance(self, instance, new, row_number=None, **kwargs):
        #add_or_update_row_teilprojekt(self.data)
    
        obj, created = Teilprojekt.objects.get_or_create(
        fkz=self.data['fkz']
    )   
        if Enargus.objects.order_by('enargus_id').last() is None:
            next_id=1
        else:
            next_id = Enargus.objects.order_by('enargus_id').last().enargus_id + 1
        #   print(next_id)
        if obj.enargus_daten is None:
            obj.enargus_daten,created=Enargus.objects.get_or_create(enargus_id=next_id)
            obj.save()
            
            
        
        #Base Enargus
        obj.enargus_daten.datenbank=self.data['Datenbank']
        obj.enargus_daten.thema=self.data['Thema']
        obj.enargus_daten.verbundbezeichnung=self.data['Verbundbezeichung']
        obj.enargus_daten.kurzbeschreibung_de=self.data['Kurzbeschreibung_de']
        obj.enargus_daten.kurzbeschreibung_en=self.data['Kurzbeschreibung_en']
        obj.enargus_daten.foerdersumme=self.data['Foerdersumme_EUR']
        obj.enargus_daten.laufzeitbeginn=self.data['Laufzeitbeginn']
        obj.enargus_daten.laufzeitende=self.data['Laufzeitende']
        obj.enargus_daten.save(update_fields=['datenbank','verbundbezeichnung','thema','kurzbeschreibung_en','kurzbeschreibung_de','foerdersumme','laufzeitbeginn','laufzeitende']) 


        #Projektleiter
      
        obj.enargus_daten.projektleiter,created=Person.objects.get_or_create(name=self.data['Name_pl'],titel=self.data['Titel_pl'],vorname=self.data['Vorname_pl'],email=self.data['Email_pl'])
        obj.enargus_daten.save(update_fields=['projektleiter'])
    
        
        
        #Leistung_sys
       
        obj.enargus_daten.leistungsplan_systematik,created=Leistung_sys.objects.get_or_create(leistungsplansystematik_nr=self.data['Leistungsplan_Sys_Nr'])
        obj.enargus_daten.leistungsplan_systematik.leistungsplansystematik_text=self.data['Leistungsplan_Sys_Text']
        obj.enargus_daten.leistungsplan_systematik.save(update_fields=['leistungsplansystematik_text'])
        #obj.enargus_daten.leistungsplan_systematik.leistungsplansystematik_text=self.data['Leistungsplan_Sys_Text']
        obj.enargus_daten.save(update_fields=['leistungsplan_systematik'])
   
       
        #Forschung
      
        obj.enargus_daten.forschung,created=Forschung.objects.get_or_create(bundesministerium=self.data['Bundesministerium'],projekttraeger=self.data['Projekttraeger'],forschungsprogramm=self.data['Forschungsprogramm'],foerderprogramm=self.data['Foerderprogramm'])
        obj.enargus_daten.save(update_fields=['forschung'])

        

        # Ausfuehrende_stelle_adresse
        obj2,created=Anschrift.objects.get_or_create(plz=self.data['PLZ_AS'],ort=self.data['Ort_AS'],land=self.data['Land_AS'],adresse=self.data['Adress_AS'])
        
       
        #Ausfuehrende_stelle
        
        obj.enargus_daten.ausfuehrende_stelle,created=Ausfuehrende_stelle.objects.get_or_create(name=self.data['Name_AS'],anschrift_id=obj2.anschrift_id)
        obj.enargus_daten.save(update_fields=['ausfuehrende_stelle'])   
      

        #Zuwendngs_empf adresse
        obj3,created=Anschrift.objects.get_or_create(plz=self.data['PLZ_ZWE'],ort=self.data['Ort_ZWE'],land=self.data['Land_ZWE'],adresse=self.data['Adress_ZWE'])
     
        
        #Zuwendungsempfaenger
        
        obj.enargus_daten.zuwendsempfanger,created=Zuwendungsempfaenger.objects.get_or_create(name=self.data['Name_ZWE'],anschrift_id=obj3.anschrift_id)
        obj.enargus_daten.save(update_fields=['zuwendsempfanger'])   

        
        #Rest

        
        
       
        
       
    #leistungsplan_systematik
    #zuwendsempfanger 
    #ausfuehrende_stelle 
    #projektleiter
    #forschung


    #foerdersumme 
    #Laufzeitbeginn
    # laufzeit ende


class TeilprojektsAdmin( ImportExportModelAdmin,ImportMixin,admin.ModelAdmin):
    def process_import(self, request, *args, **kwargs):
        """
        Perform the actual import action (after the user has confirmed the import)
        """
        del self.impf
        del self.impfor
        del self.tmp
        del self.frm
        if 'decline' in request.POST:
            return redirect(request.META.get('HTTP_REFERER'))
        if not self.has_import_permission(request):
            raise PermissionDenied
        form_type = self.get_confirm_import_form()
        confirm_form = form_type(request.POST)
        if confirm_form.is_valid():
            import_formats = self.get_import_formats()
            input_format = import_formats[
                int(confirm_form.cleaned_data['input_format'])
            ]()
            tmp_storage = self.get_tmp_storage_class()(name=confirm_form.cleaned_data['import_file_name'])
            data = tmp_storage.read(input_format.get_read_mode())
            if not input_format.is_binary() and self.from_encoding:
                data = force_str(data, self.from_encoding)
            dataset = input_format.create_dataset(data)

            result = self.process_dataset(dataset, confirm_form, request, *args, **kwargs)

            tmp_storage.remove()
        

            return self.process_result(result, request)

    def import_action(self, request, *args, **kwargs):
        """
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        """
        if not self.has_import_permission(request):
            raise PermissionDenied

        context = self.get_import_context_data()
       
        import_formats = self.get_import_formats()
        form_type = self.get_import_form()
        form_kwargs = self.get_form_kwargs(form_type, *args, **kwargs)


        
        try:
            #1/form.is_valid()
            1/self.frm.is_valid()
            form=self.frm
            #   print('nononon')
        except:
            form = form_type(import_formats,
                            request.POST or None,
                            request.FILES or None,
                            **form_kwargs)
            self.frm=form
            #print('hello')
        finally:
            #print( form.is_valid())
            if request.POST and form.is_valid():
                if 'Report_Skipped' in request.POST:

                    self.resource_class._meta.report_skipped=not(self.resource_class._meta.report_skipped)
                    input_format=self.impfor
                    tmp_storage = self.tmp
                    import_file=self.impf
                else:
                    input_format = import_formats[
                        int(form.cleaned_data['input_format'])
                    ]()
                    self.impfor=input_format
                    import_file = form.cleaned_data['import_file']
                    self.impf=import_file
                    # first always write the uploaded file to disk as it may be a
                    # memory file or else based on settings upload handlers
                    tmp_storage = self.write_to_tmp_storage(import_file, input_format)
                    self.tmp=tmp_storage

                # then read the file, using the proper format-specific mode
                # warning, big files may exceed memory
                try:
                    data = tmp_storage.read(input_format.get_read_mode())
                    if not input_format.is_binary() and self.from_encoding:
                        data = force_str(data, self.from_encoding)
                    dataset = input_format.create_dataset(data)
                except UnicodeDecodeError as e:
                    return HttpResponse(_(u"<h1>Imported file has a wrong encoding: %s</h1>" % e))
                except Exception as e:
                    return HttpResponse(_(u"<h1>%s encountered while trying to read file: %s</h1>" % (type(e).__name__, import_file.name)))

                # prepare kwargs for import data, if needed
                res_kwargs = self.get_import_resource_kwargs(request, form=form, *args, **kwargs)
                resource = self.get_import_resource_class()(**res_kwargs)
                

                
                # prepare additional kwargs for import_data, if needed
                imp_kwargs = self.get_import_data_kwargs(request, form=form, *args, **kwargs)
                result = resource.import_data(dataset, dry_run=True,
                                            raise_errors=False,
                                            file_name=import_file.name,
                                            user=request.user,
                                            **imp_kwargs)

                context['result'] = result

                if not result.has_errors() and not result.has_validation_errors():
                    initial = {
                        'import_file_name': tmp_storage.name,
                        'original_file_name': import_file.name,
                        'input_format': form.cleaned_data['input_format'],
                    }
                    confirm_form = self.get_confirm_import_form()
                    initial = self.get_form_kwargs(form=form, **initial)
                    context['confirm_form'] = confirm_form(initial=initial)
            else:
                res_kwargs = self.get_import_resource_kwargs(request, form=form, *args, **kwargs)
                resource = self.get_import_resource_class()(**res_kwargs)

            context.update(self.admin_site.each_context(request))

            context['title'] = _("Import")
            context['form'] = form
            context['opts'] = self.model._meta
            context['fields'] = [f.column_name for f in resource.get_user_visible_fields()]
            request.current_app = self.admin_site.name
            
            return TemplateResponse(request, [self.import_template_name],
                                    context)

    resource_class = TeilProjektResource
        

admin.site.register(Teilprojekt,TeilprojektsAdmin)
#class EnargusAdmin( ImportExportModelAdmin ):