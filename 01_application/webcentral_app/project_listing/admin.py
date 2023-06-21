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

admin.site.register(FurtherFundingInformation)
admin.site.register(Questionnaire2021)
admin.site.register(GrantRecipient)
admin.site.register(ExecutingEntity)
admin.site.register(Person)
admin.site.register(Address)


admin.site.register(Enargus)

class SubprojectResource(resources.ModelResource,ImportMixin):
    
    #widget=ForeignKeyWidget(Enargus,'enargus_id')
   
    
    database=fields.Field(
        attribute='enargusData__database',
        column_name='Datenbank',
        widget=CharWidget()  
    )
        
      
    topics=fields.Field(
        attribute='enargusData__topics',
        column_name='topics',
        widget=CharWidget()
        
    )

    collaborativeProject=fields.Field(
        attribute='enargusData__collaborativeProject',
        column_name='Verbundbezeichung',
        widget=CharWidget()
    
        
    )  
    
    shortDescriptionDe=fields.Field(
        attribute='enargusData__shortDescriptionDe',
        column_name='Kurzbeschreibung_de',
        widget=CharWidget()
    
        
    )
    shortDescriptionEn=fields.Field(
        attribute='enargusData__shortDescriptionEn',
        column_name='Kurzbeschreibung_en',
        widget=CharWidget()
    
        
    )
    projectLead=fields.Field(
        attribute='enargusData__projectLead__surname',
        column_name='nameProjectLead',
        widget=CharWidget()   
    )
    projectLeadFirstName=fields.Field(
        attribute='enargusData__projectLead__vorname',
        column_name='firstNameProjectLead',
        widget=CharWidget()   
    )
    projectLeadEmail=fields.Field(
        attribute='enargusData__projectLead__email',
        column_name='Email_pl',
        widget=CharWidget()   
    )
    projectLeadTitle=fields.Field(
        attribute='enargusData__projectLead__title',
        column_name='titleProjectLead',
        widget=CharWidget()   
    )

    startDate=fields.Field(
        attribute='enargusData__startDate',
        column_name='Laufzeitbeginn', ##
        widget=DateWidget()   
    )
    endDate=fields.Field(
        attribute='enargusData__endDate',
        column_name='Laufzeitende',###
        widget=DateWidget()   
    )
    appropriatedBudget=fields.Field(
        attribute='enargusData__appropriatedBudget',
        column_name='Foerdersumme_EUR',###
        widget=DecimalWidget()
         
    )
    
    rAndDPlanningCategoryNumber=fields.Field(
        attribute='enargusData__rAndDPlanningCategory__rAndDPlanningCategoryNumber',
        column_name='Leistungsplan_Sys_Nr',###
        widget=CharWidget()   
    )
    rAndDPlanningCategoryText=fields.Field(
        attribute='enargusData__rAndDPlanningCategory__rAndDPlanningCategoryText',
        column_name='Leistungsplan_Sys_Text',###
        widget=CharWidget()   
    )
  
    executingEntityName=fields.Field(
        attribute='enargusData__executingEntity__surname',
        column_name='Name_AS',###
        widget=CharWidget()   
    )
    executingEntityPlz=fields.Field(
        attribute='enargusData__executingEntity__address__plz',
        column_name='PLZ_AS',###
        widget=CharWidget()   
    )
    executingEntityLocation=fields.Field(
        attribute='enargusData__executingEntity__address__ort',
        column_name='Ort_AS',###
        widget=CharWidget()   
    )
    executingEntityAddress=fields.Field(
        attribute='enargusData__executingEntity__address__address',
        column_name='Adress_AS',###
        widget=CharWidget()   
    )
    executingEntityState=fields.Field(
        attribute='enargusData__executingEntity__address__land',
        column_name='Land_AS',###
        widget=CharWidget()   
    )
    
    grantRecipientName=fields.Field(
        attribute='enargusData__grantRecipient__surname',
        column_name='Name_ZWE',###
        widget=CharWidget()   
    )
    grantRecipientPlz=fields.Field(
        attribute='enargusData__grantRecipient__address__plz',
        column_name='PLZ_ZWE',###
        widget=CharWidget()   
    )
    grantRecipientLocation=fields.Field(
        attribute='enargusData__grantRecipient__address__ort',
        column_name='Ort_ZWE',###
        widget=CharWidget()   
    )
    grantRecipientState=fields.Field(
        attribute='enargusData__grantRecipient__address__land',
        column_name='Land_ZWE',###
        widget=CharWidget()   
    )
    grantRecipientAddress=fields.Field(
        attribute='enargusData__grantRecipient__address__address',
        column_name='Adress_ZWE',###
        widget=CharWidget()   
    )
    fundedBy=fields.Field(
        attribute='enargusData__furtherFundingInformation__fundedBy',
        column_name='Bundesministerium',###
        widget=CharWidget()   
    )

    projectManagementAgency=fields.Field(
        attribute='enargusData__furtherFundingInformation__projectManagementAgency',
        column_name='Projekttraeger',###
        widget=CharWidget()   
    )

    researchProgram=fields.Field(
        attribute='enargusData__furtherFundingInformation__researchProgram',
        column_name='Forschungsprogramm',###
        widget=CharWidget()   
    )

    fundingProgram=fields.Field(
        attribute='enargusData__furtherFundingInformation__fundingProgram',
        column_name='Foerderprogramm',###
        widget=CharWidget()   
    )
    

    
    

    list_attrb=['enargusData__database', 'enargusData__topics', 'enargusData__collaborativeProject', 
    'enargusData__shortDescriptionDe', 'enargusData__shortDescriptionEn', 'enargusData__projectLead__surname', 
    'enargusData__projectLead__firstName', 'enargusData__projectLead__email', 'enargusData__projectLead__title',
    'enargusData__startDate', 'enargusData__endDate', 'enargusData__appropriatedBudget','enargusData__rAndDPlanningCategory__rAndDPlanningCategoryNumber', 
    'enargusData__rAndDPlanningCategory__rAndDPlanningCategoryText', 'enargusData__executingEntity__surname', 'enargusData__executingEntity__address__plz', 
    'enargusData__executingEntity__address__location', 'enargusData__executingEntity__address__address', 'enargusData__executingEntity__address__state', 
    'enargusData__grantRecipient__surname', 'enargusData__grantRecipient__address__plz', 'enargusData__grantRecipient__address__location', 'enargusData__grantRecipient__address__state', 
    'enargusData__grantRecipient__address__address', 'enargusData__furtherFundingInformation__fundedBy', 'enargusData__furtherFundingInformation__projectManagementAgency', 'enargusData__furtherFundingInformation__researchProgram', 
    'enargusData__furtherFundingInformation__fundingProgram', 'referenceNumber_id', 'enargusData', 'moduleAssignment', 'schlagwortregister_erstsichtung', 'fragebogen_21']
    
    class Meta:
        model   =   Subproject
        import_id_fields = ['referenceNumber_id']
        
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
            return False
        for field in self.get_import_fields():
            #print(field)
            try:
                # For fields that are models.fields.related.ManyRelatedManager
                # we need to compare the results
                if list(field.get_value(instance).all()) != list(field.get_value(original).all()):
                    return False
            except AttributeError:
                if ((field.get_value(instance)) != field.get_value(original)):
                    try:
                        if (field.get_value(instance).date()==field.get_value(original)):
                            continue
                    except:
                        pass

                    return False
        return True
        
 
          
    def before_import_row(self, row, row_number=None, **kwargs):
        self.data=row
        set=True
        #print(self.backup['database'].attribute)
        #print(self.backup['database'].attribute)
        #print(type(self.fields))

        if not Subproject.objects.filter(referenceNumber_id=row['fkz']).exists():
            #for f in self.get_export_order():
             #   i=0
              #  if f !='fkz' :
               #     self.fields[f].attribute=lst[i]
                #    i+=1
            self.fields['startDate'].attribute='ebbbb'
            self.fields['endDate'].attribute='epppp'
            self.fields['grantRecipientName'].attribute='enarten'
            self.fields['grantRecipientPlz'].attribute='enargusen'
            self.fields['grantRecipientLocation'].attribute='enarguen'
            self.fields['grantRecipientState'].attribute='enaaten'
            self.fields['grantRecipientAddress'].attribute='enargen'
            self.fields['projectLeadTitle'].attribute='enargus_dn'
            self.fields['projectLeadSurname'].attribute='enargus_ten'
            self.fields['projectLeadFirstName'].attribute='en'
            self.fields['projectLeadEmail'].attribute='enars_ten'
            self.fields['executingEntityPlz'].attribute='needstochange'
            self.fields['executingEntityState'].attribute='ena'
            self.fields['executingEntityLocation'].attribute='enb'
            self.fields['executingEntityName'].attribute='enc'
            self.fields['executingEntityAddress'].attribute='enpppp'
            self.fields['database'].attribute='enmmm'
            self.fields['topics'].attribute='errr'
            self.fields['rAndDPlanningCategoryNumber'].attribute='ennnnnnnnnnn'
            self.fields['rAndDPlanningCategoryText'].attribute='ekkkkkkkkkkkkkk'
            self.fields['shortDescriptionDe'].attribute='else'
            self.fields['shortDescriptionEn'].attribute='eooooo'
            self.fields['fundingProgram'].attribute='epooo'
            self.fields['researchProgram'].attribute='whatever'
            self.fields['projectManagementAgency'].attribute='enargi'
            self.fields['fundedBy'].attribute='enargo'
            self.fields['collaborativeProject'].attribute='enargiii'
            self.fields['appropriatedBudget'].attribute='buggy'

            #self.fields['executingEntityAddress'].attribute='enarg'
            
            set=False

        else:
            if (not Subproject.objects.get(referenceNumber_id=row['fkz']).enargusData.projectLead):
                self.fields['projectLeadTitle'].attribute='enargus_dn'
                self.fields['projectLeadSurname'].attribute='enargus_ten'
                self.fields['projectLeadFirstName'].attribute='en'
                self.fields['projectLeadEmail'].attribute='enars_ten'
                set=False

            if (not Subproject.objects.get(referenceNumber_id=row['fkz']).enargusData.grantRecipient):
                self.fields['grantRecipientName'].attribute='enarten'
                self.fields['grantRecipientPlz'].attribute='enargusen'
                self.fields['grantRecipientLocation'].attribute='enarguen'
                self.fields['grantRecipientState'].attribute='enaaten'
                self.fields['grantRecipientAddress'].attribute='enargen'
                set=False

            if (not Subproject.objects.get(referenceNumber_id=row['fkz']).enargusData.ExecutingEntity):
                self.fields['executingEntityPlz'].attribute='noooo'
                self.fields['executingEntityState'].attribute='ena'
                self.fields['executingEntityLocation'].attribute='enb'
                self.fields['executingEntityName'].attribute='enc'
                self.fields['executingEntityAddress'].attribute='enpppp'
                set=False

            if (not Subproject.objects.get(referenceNumber_id=row['fkz']).enargusData.rAndDPlanningCategory):
                self.fields['leisstungplan_nr'].attribute='ennnnnnnnnnn'
                self.fields['leisstungplan_txt'].attribute='ekkkkkkkkkkkkkk'
                set=False
        
        if set ==True:

            i=0

            for f in self.get_export_order():
                self.fields[f].attribute=self.list_attrb[i]
                i=i+1
 

     
    
   

    def after_save_instance(self, instance, new, row_number=None, **kwargs):
        #add_or_update_row_teilprojekt(self.data)
    
        obj, created = Subproject.objects.get_or_create(
        referenceNumber_id=self.data['fkz']
    )   
        if Enargus.objects.order_by('enargus_id').last() is None:
            next_id=1
        else:
            next_id = Enargus.objects.order_by('enargus_id').last().enargus_id + 1
        #   print(next_id)
        if obj.enargusData is None:
            obj.enargusData,created=Enargus.objects.get_or_create(enargus_id=next_id)
            obj.save()
            
            
        
        #Base Enargus
        obj.enargusData.database=self.data['Datenbank']
        obj.enargusData.topics=self.data['Thema']
        obj.enargusData.collaborativeProject=self.data['Verbundbezeichung']
        obj.enargusData.shortDescriptionDe=self.data['Kurzbeschreibung_de']
        obj.enargusData.shortDescriptionEn=self.data['Kurzbeschreibung_en']
        obj.enargusData.appropriatedBudget=self.data['Foerdersumme_EUR']
        obj.enargusData.startDate=self.data['Laufzeitbeginn']
        obj.enargusData.endDate=self.data['Laufzeitende']
        obj.enargusData.save(update_fields=['database','collaborativeProject','topics','shortDescriptionEn','shortDescriptionDe','appropriatedBudget','startDate','endDate']) 


        #Projektleiter
      
        obj.enargusData.projectLead,created=Person.objects.get_or_create(name=self.data['Name_pl'],titel=self.data['Titel_pl'],vorname=self.data['Vorname_pl'],email=self.data['Email_pl'])
        obj.enargusData.save(update_fields=['projectLead'])
    
        
        
        #RAndDPlanningCategory
       
        obj.enargusData.rAndDPlanningCategory,created=RAndDPlanningCategory.objects.get_or_create(rAndDPlanningCategoryNumber=self.data['Leistungsplan_Sys_Nr'])
        obj.enargusData.rAndDPlanningCategory.rAndDPlanningCategoryText=self.data['Leistungsplan_Sys_Text']
        obj.enargusData.rAndDPlanningCategory.save(update_fields=['rAndDPlanningCategoryText'])
        #obj.enargusData.rAndDPlanningCategory.rAndDPlanningCategoryText=self.data['Leistungsplan_Sys_Text']
        obj.enargusData.save(update_fields=['rAndDPlanningCategory'])
   
       
        #furtherFundingInformation
      
        obj.enargusData.furtherFundingInformation,created=FurtherFundingInformation.objects.get_or_create(fundedBy=self.data['Bundesministerium'],projectManagementAgency=self.data['Projekttraeger'],forschungsprogramm=self.data['Forschungsprogramm'],foerderprogramm=self.data['Foerderprogramm'])
        obj.enargusData.save(update_fields=['furtherFundingInformation'])

        

        # Ausfuehrende_stelle_adresse
        obj2,created=Address.objects.get_or_create(plz=self.data['PLZ_AS'],location=self.data['Ort_AS'],state=self.data['Land_AS'],address=self.data['Adress_AS'])
        
       
        #ExecutingEntity
        
        obj.enargusData.executingEntity,created=ExecutingEntity.objects.get_or_create(name=self.data['Name_AS'],address_id=obj2.address_id)
        obj.enargusData.save(update_fields=['executingEntity'])   
      

        #Zuwendngs_empf adresse
        obj3,created=Address.objects.get_or_create(plz=self.data['PLZ_ZWE'],location=self.data['Ort_ZWE'],state=self.data['Land_ZWE'],address=self.data['Adress_ZWE'])
     
        
        #GrantRecipient
        
        obj.enargusData.grantRecipient,created=GrantRecipient.objects.get_or_create(name=self.data['Name_ZWE'],address_id=obj3.address_id)
        obj.enargusData.save(update_fields=['grantRecipient'])   

        
        #Rest

        
        
       
        
       
    #rAndDPlanningCategory
    #grantRecipient 
    #ExecutingEntity 
    #projectLead
    #furtherFundingInformation


    #appropriatedBudget 
    #startDate
    #endDate


class SubrojectAdmin(ImportExportModelAdmin,ImportMixin,admin.ModelAdmin):
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

    resource_class = SubprojectResource
    search_fields=['referenceNumber_id',]
        

admin.site.register(Subproject,SubrojectAdmin)
#class EnargusAdmin( ImportExportModelAdmin ):


##############################################


class ModuleAssignment_Resource(resources.ModelResource,ImportMixin):
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

            return False
        for field in self.get_import_fields():
            #print(field)
            try:
                # For fields that are models.fields.related.ManyRelatedManager
                # we need to compare the results
                if list(field.get_value(instance).all()) != list(field.get_value(original).all()):
                    
                    return False
            except AttributeError:
                if (field.get_value(instance) != field.get_value(original)) :  

                    print(field.get_value(instance))
                    print(field.get_value(original))

                    return False
        return True
    priority1=fields.Field(
        column_name='modulzuordnung_ptj_1',
        widget=CharWidget()  
    )
    priority2=fields.Field(
        column_name='modulzuordnung_ptj_2',
        widget=CharWidget()  
    )
    priority3=fields.Field(
        column_name='modulzuordnung_ptj_3',
        widget=CharWidget()  
    )
    priority4=fields.Field(
        column_name='modulzuordnung_ptj_4',
        widget=CharWidget()  
    )
    class Meta:
        model   =   Subproject
        fields=('fkz,')
        import_id_fields = ['fkz']
        skip_unchanged = True
        report_skipped=False

    def before_import_row(self, row, row_number=None, **kwargs):
            self.data=row

            if (not Subproject.objects.filter(referenceNumber_id=row['fkz']).exists()) or (not Subproject.objects.get(referenceNumber_id=row['fkz']).moduleAssignment):

                self.fields['priority4'].attribute='ebbbb'
                self.fields['priority3'].attribute='epppp'
                self.fields['priority2'].attribute='enarten'
                self.fields['priority1'].attribute='enaen'
                
            else:
                self.fields['priority4'].attribute='zuordnung__priority_4'
                self.fields['priority3'].attribute='zuordnung__priority_3'
                self.fields['priority2'].attribute='zuordnung__priority_2'
                self.fields['priority1'].attribute='zuordnung__priority_1'

    def after_save_instance(self, instance, new, row_number=None, **kwargs):
        obj, created = Subproject.objects.get_or_create(referenceNumber_id=self.data['fkz'])
        obj.moduleAssignment,created=ModuleAssignment.objects.get_or_create(priority1=self.data['modulzuordnung_ptj_1'],priority2=self.data['modulzuordnung_ptj_2'],priority3=self.data['modulzuordnung_ptj_3'],priority4=self.data['modulzuordnung_ptj_4'])
        obj.save(update_fields=['assignment'])   

class ModulZuordnungAdmin(ImportExportModelAdmin,ImportMixin,admin.ModelAdmin):
    resource_class = ModuleAssignment_Resource
               
admin.site.register(ModuleAssignment,ModulZuordnungAdmin)  
