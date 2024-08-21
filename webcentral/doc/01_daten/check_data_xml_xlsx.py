#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import sys


# In[2]:


# aktuelle Arbeitsverzeichnis anpassen (soll das Verzeichnis sein, in dem das
# Skipt liegt, relative Pfade sind darauf ausgerichtet)
os.chdir('/home/cudok/Documents/GitHub/projektliste_bf/')


# In[3]:


path_modules = os.path.join(
    '../../GitHub/dvg_lib/ProjektListe/')  # zeigt auf den Ordner indem die
                                   # Datei auswertung.pytung.py liegt
sys.path.append(path_modules)
import auswertung as asw


# In[4]:


#pip freeze


# # Einlesen

# In[5]:


list_spalten = '02_Parameter_Dateien/Spalten_xml2csv_Vergl.csv'
xml2csv = '02_Parameter_Dateien/Spalten_dict_xml2csv_Vergl.csv'
path_xml = "../../../Nextcloud/Shared/Digitale_Vernetzung/Assis/03_Projekte/DVG0001_BMWi_Wende/12_Daten/01_Enargus/Daten_von_Bosch_2022_02_01/enargus.xml"


# In[6]:


df = asw.read_xml_enargus(path_xml, xml2csv, list_spalten)


# In[7]:


df.info()


# In[8]:


#cols_vec = asw.read_spalten_vor_csv('02_Parameter_Dateien/Spalten_xml2csv_Vergl.csv')
#cols_vec


# In[9]:


#namenspaces_enargus = {'':"http://www.enargus.de/elements/0.1/begleitforschung/", 'bscw':"http://bscw.de/bscw/elements/0.1/"}


# In[10]:


#cols = ['FKZ', 'Datenbank', 'Laufzeitbeginn']
#col_dic = {'FKZ':'fkz', 'Datenbank':'db', 'Laufzeitbeginn':'fi_von/iso8601'}
#df_test = asw.read_xml(path_xml,col_dic, cols, namespaces=namenspaces_enargus)


# In[11]:


#df_test


# In[12]:


path_excel = '../../../Nextcloud/Shared/WenDE/12_Daten/03_Gesamt_BF_Daten/20220207_Verteiler_EWB_Projekte.xlsx'


# In[13]:


df_xlsx = pd.read_excel(path_excel, sheet_name='EnArgus Rohdaten')


# In[14]:


df_xlsx.info()


# #### xml teilweise nicht vollbesetzt
#  31  auf_bez_pub                             1419 non-null   object        
#  32  auf_bez_pub_quelle                      1419 non-null   object        
#  33  auf_bez_pub_en                          1303 non-null   object        
#  34  auf_bez_pub_en_quelle                   1303 non-null   object  
#  36  pers_titel_pl                           1305 non-null   object
#  40  laengengrad_st                          1629 non-null   float64    
#  41  breitengrad_st                          1629 non-null   float64       
#  42  Spalte1                                 0 non-null      float64 

# # Vergleich
# funktioniert noch nicht. Es liegt wahrscheinlich an den Spaltennamen

# In[15]:


#df_xlsx[['fkz', 'db']].info()


# In[16]:


#df[['fkz', 'db']].info()


# # Für 11 Projekte stimmt die excel-Datei nicht mit der xml beim Enddatum überein

# In[17]:


col_xml = ['fkz', 'db', 'v_thema', 'fi_von/iso8601', 'fi_ende/iso8601']
col_xlsx = ['fkz', 'db','v_thema']
df_xml_part = df[col_xml]
df_xlsx_part = df_xlsx[col_xlsx]
# format und name anpassen
series_start_xlsx = df_xlsx['fi_von.iso8601'].dt.strftime('%Y-%m-%d').rename('fi_von/iso8601')
df_xlsx_part = pd.concat([df_xlsx_part, series_start_xlsx], axis=1)
series_ende_xlsx = df_xlsx['fi_ende.iso8601'].dt.strftime('%Y-%m-%d').rename('fi_ende/iso8601')
df_xlsx_part = pd.concat([df_xlsx_part, series_ende_xlsx], axis=1)

df_fkz_diff = pd.concat([df_xml_part, df_xlsx_part]).drop_duplicates(keep=False)
df_fkz_diff.info()


# In[18]:


df_fkz_diff


# ### xlsx-Datei (auch in der xlsx-Datei in calc geprüft)

# In[19]:


df_xlsx_part[['fkz','fi_ende/iso8601']][df_xlsx_part['fkz']=='03ETW012D']


# ### xml-Datei (auch in der xml-Datei in firefox geprüft)

# In[20]:


df_xml_part[['fkz','fi_ende/iso8601']][df_xml_part['fkz']=='03ETW012D']


# 1. Block: xml 
# 2. Block: xlsx
# xml: Diffenzprojekte haben immer ein späteres  End-Datum
# - Vermutung: xlsx enthält die ursprünglichen/beantragten End-Daten, die Anpassung auf Grund von genehmigten Verlängerungen werden nicht in Verteiler-xlxs eingepflegt

# ## Erste Null in der PLZ bei plz_strasse_st fehlt in der xlxs-Datei 
# - weiterer Vergleich ohne Ende-Datum
# 

# - Die eigentlichen Wert der PLZ sind gleich!!
# 
# 
# - die ersten Nullen der PLZ sind schon in der xlxs nicht enthalten, dies ist noch ein Grund die nicht die xlxs als Datenquelle zu nutzen

# In[21]:


col_xml = ['fkz', 'db', 'v_thema', 'fi_von/iso8601', 'fi_sumbew/value', 'ver_bez','lp_nr','lp_text','name_st',
          'plz_strasse_st']
col_xlsx = ['fkz', 'db','v_thema','ver_bez','lp_nr','lp_text','name_st']
df_xml_part = df[col_xml]
df_xlsx_part = df_xlsx[col_xlsx]
# format und name anpassen
series_start_xlsx = df_xlsx['fi_von.iso8601'].dt.strftime('%Y-%m-%d').rename('fi_von/iso8601')
df_xlsx_part = pd.concat([df_xlsx_part, series_start_xlsx], axis=1)
series_value_xlsx = df_xlsx['fi_sumbew.value'].astype('str').rename('fi_sumbew/value')
df_xlsx_part = pd.concat([df_xlsx_part, series_value_xlsx], axis=1)

series_plz_xlsx = df_xlsx['plz_strasse_st'].astype('str')
df_xlsx_part = pd.concat([df_xlsx_part, series_plz_xlsx], axis=1)


df_fkz_diff = pd.concat([df_xml_part, df_xlsx_part]).drop_duplicates(keep=False)
df_fkz_diff.info()


# In[22]:


df_group = df_fkz_diff[['fkz','plz_strasse_st']].groupby(['fkz'])
df_group.groups


# ## 3 Abweichungen bei ad_str_st 
# - weiterer Vergleich ohne Ende-Datum und PLZ

# In[23]:


col_xml = ['fkz', 'db', 'v_thema', 'fi_von/iso8601', 'fi_sumbew/value', 'ver_bez','lp_nr','lp_text','name_st',
          'ort_st','ad_str_st']
col_xlsx = ['fkz', 'db','v_thema','ver_bez','lp_nr','lp_text','name_st','ort_st','ad_str_st']
df_xml_part = df[col_xml]
df_xlsx_part = df_xlsx[col_xlsx]
# format und name anpassen
series_start_xlsx = df_xlsx['fi_von.iso8601'].dt.strftime('%Y-%m-%d').rename('fi_von/iso8601')
df_xlsx_part = pd.concat([df_xlsx_part, series_start_xlsx], axis=1)
series_value_xlsx = df_xlsx['fi_sumbew.value'].astype('str').rename('fi_sumbew/value')
df_xlsx_part = pd.concat([df_xlsx_part, series_value_xlsx], axis=1)




df_fkz_diff = pd.concat([df_xml_part, df_xlsx_part]).drop_duplicates(keep=False)
df_fkz_diff.info()


# In[24]:


df_fkz_diff[['fkz','ad_str_st']]


# ## Erste Null in der PLZ bei plz_strasse_ze fehlt in der xlxs-Datei 
# - weiterer Vergleich ohne Ende-Datum, plz_strasse_st und ad_str_st

# - Die eigentlichen Wert der PLZ sind gleich!!
# 
# 
# - die ersten Nullen der PLZ sind schon in der xlxs nicht enthalten, dies ist noch ein Grund die nicht die xlxs als Datenquelle zu nutzen

# In[52]:


col_xml = ['fkz', 'db', 'v_thema', 'fi_von/iso8601', 'fi_sumbew/value', 'ver_bez','lp_nr','lp_text','name_st',
          'ort_st','land_st','gem_gemkz_st','name_ze','plz_strasse_ze']
col_xlsx = ['fkz', 'db','v_thema','ver_bez','lp_nr','lp_text','name_st','ort_st','land_st','name_ze']
df_xml_part = df[col_xml]
df_xlsx_part = df_xlsx[col_xlsx]
# format und name anpassen
series_start_xlsx = df_xlsx['fi_von.iso8601'].dt.strftime('%Y-%m-%d').rename('fi_von/iso8601')
df_xlsx_part = pd.concat([df_xlsx_part, series_start_xlsx], axis=1)
series_value_xlsx = df_xlsx['fi_sumbew.value'].astype('str').rename('fi_sumbew/value')
df_xlsx_part = pd.concat([df_xlsx_part, series_value_xlsx], axis=1)
series_gemkz_xlsx = df_xlsx['gem_gemkz_st'].astype('str')
df_xlsx_part = pd.concat([df_xlsx_part, series_gemkz_xlsx], axis=1)
series_plz_ze_xlsx = df_xlsx['plz_strasse_ze'].astype('str')
df_xlsx_part = pd.concat([df_xlsx_part, series_plz_ze_xlsx], axis=1)


df_fkz_diff = pd.concat([df_xml_part, df_xlsx_part]).drop_duplicates(keep=False)
df_fkz_diff.info()


# In[53]:


df_group = df_fkz_diff[['fkz','plz_strasse_ze']].groupby(['fkz'])
df_group.groups


# ## 2 Abweichungen in ad_str_ze
# - weiterer Vergleich ohne Ende-Datum, plz_strasse_st, ad_str_st, plz_strasse_ze

# In[63]:


col_xml = ['fkz', 'db', 'v_thema', 'fi_von/iso8601', 'fi_sumbew/value', 'ver_bez','lp_nr','lp_text','name_st',
          'ort_st','land_st','gem_gemkz_st','name_ze', 'ort_ze', 'ad_str_ze']
col_xlsx = ['fkz', 'db','v_thema','ver_bez','lp_nr','lp_text','name_st','ort_st','land_st','name_ze', 
            'ort_ze', 'ad_str_ze']
df_xml_part = df[col_xml]
df_xlsx_part = df_xlsx[col_xlsx]
# format und name anpassen
series_start_xlsx = df_xlsx['fi_von.iso8601'].dt.strftime('%Y-%m-%d').rename('fi_von/iso8601')
df_xlsx_part = pd.concat([df_xlsx_part, series_start_xlsx], axis=1)
series_value_xlsx = df_xlsx['fi_sumbew.value'].astype('str').rename('fi_sumbew/value')
df_xlsx_part = pd.concat([df_xlsx_part, series_value_xlsx], axis=1)
series_gemkz_xlsx = df_xlsx['gem_gemkz_st'].astype('str')
df_xlsx_part = pd.concat([df_xlsx_part, series_gemkz_xlsx], axis=1)



df_fkz_diff = pd.concat([df_xml_part, df_xlsx_part]).drop_duplicates(keep=False)
df_fkz_diff.info()


# In[64]:


df_fkz_diff[['fkz','ad_str_ze']]


# ## 6 Abweichungen in pers_pl
# - weiterer Vergleich ohne Ende-Datum, plz_strasse_st, ad_str_st, plz_strasse_ze, ad_str_ze
# - ohne auf_bez_pub_quelle_en, weil keine Einträge in xml und keine Spalte in xlsx

# In[80]:


col_xml = ['fkz', 'db', 'v_thema', 'fi_von/iso8601', 'fi_sumbew/value', 'ver_bez','lp_nr','lp_text','name_st',
          'ort_st','land_st','gem_gemkz_st','name_ze', 'ort_ze', 'land_ze', 'gem_gemkz_ze', 'v_ressort', 
           'v_pt_detail', 'v_forschsp_text','v_prog_text', 'auf_bez_pub', 'auf_bez_pub_quelle', 'auf_bez_pub_en',
          'pers_pl']
col_xlsx = ['fkz', 'db','v_thema','ver_bez','lp_nr','lp_text','name_st','ort_st','land_st','name_ze', 
            'ort_ze', 'land_ze','v_ressort', 'v_pt_detail','v_forschsp_text', 'v_prog_text', 'auf_bez_pub',
           'auf_bez_pub_quelle', 'auf_bez_pub_en', 'pers_pl']
df_xml_part = df[col_xml]
df_xlsx_part = df_xlsx[col_xlsx]
# format und name anpassen
series_start_xlsx = df_xlsx['fi_von.iso8601'].dt.strftime('%Y-%m-%d').rename('fi_von/iso8601')
df_xlsx_part = pd.concat([df_xlsx_part, series_start_xlsx], axis=1)
series_value_xlsx = df_xlsx['fi_sumbew.value'].astype('str').rename('fi_sumbew/value')
df_xlsx_part = pd.concat([df_xlsx_part, series_value_xlsx], axis=1)
series_gemkz_xlsx = df_xlsx['gem_gemkz_st'].astype('str')
df_xlsx_part = pd.concat([df_xlsx_part, series_gemkz_xlsx], axis=1)
series_gemkz_ze_xlsx = df_xlsx['gem_gemkz_ze'].astype('str')
df_xlsx_part = pd.concat([df_xlsx_part, series_gemkz_ze_xlsx], axis=1)


df_fkz_diff = pd.concat([df_xml_part, df_xlsx_part]).drop_duplicates(keep=False)
df_fkz_diff.info()


# In[82]:


df_fkz_diff[['fkz','pers_pl']]


# ## 1 Abweichungen in pers_titel_pl
# - weiterer Vergleich ohne Ende-Datum, plz_strasse_st, ad_str_st, plz_strasse_ze, ad_str_ze, pers_pl
# - ohne auf_bez_pub_quelle_en, weil keine Einträge in xml und keine Spalte in xlsx

# In[85]:


col_xml = ['fkz', 'db', 'v_thema', 'fi_von/iso8601', 'fi_sumbew/value', 'ver_bez','lp_nr','lp_text','name_st',
          'ort_st','land_st','gem_gemkz_st','name_ze', 'ort_ze', 'land_ze', 'gem_gemkz_ze', 'v_ressort', 
           'v_pt_detail', 'v_forschsp_text','v_prog_text', 'auf_bez_pub', 'auf_bez_pub_quelle', 'auf_bez_pub_en'
          , 'pers_titel_pl']
col_xlsx = ['fkz', 'db','v_thema','ver_bez','lp_nr','lp_text','name_st','ort_st','land_st','name_ze', 
            'ort_ze', 'land_ze','v_ressort', 'v_pt_detail','v_forschsp_text', 'v_prog_text', 'auf_bez_pub',
           'auf_bez_pub_quelle', 'auf_bez_pub_en', 'pers_titel_pl']
df_xml_part = df[col_xml]
df_xlsx_part = df_xlsx[col_xlsx]
# format und name anpassen
series_start_xlsx = df_xlsx['fi_von.iso8601'].dt.strftime('%Y-%m-%d').rename('fi_von/iso8601')
df_xlsx_part = pd.concat([df_xlsx_part, series_start_xlsx], axis=1)
series_value_xlsx = df_xlsx['fi_sumbew.value'].astype('str').rename('fi_sumbew/value')
df_xlsx_part = pd.concat([df_xlsx_part, series_value_xlsx], axis=1)
series_gemkz_xlsx = df_xlsx['gem_gemkz_st'].astype('str')
df_xlsx_part = pd.concat([df_xlsx_part, series_gemkz_xlsx], axis=1)
series_gemkz_ze_xlsx = df_xlsx['gem_gemkz_ze'].astype('str')
df_xlsx_part = pd.concat([df_xlsx_part, series_gemkz_ze_xlsx], axis=1)


df_fkz_diff = pd.concat([df_xml_part, df_xlsx_part]).drop_duplicates(keep=False)
df_fkz_diff.info()


# In[86]:


df_fkz_diff[['fkz','pers_titel_pl']]


# ## 7 Abweichungen in pers_vname_pl + pers_name_pl + pers_email_pl
# - weiterer Vergleich ohne Ende-Datum, plz_strasse_st, ad_str_st, plz_strasse_ze, ad_str_ze, pers_pl, pers_titel_pl
# - ohne auf_bez_pub_quelle_en, weil keine Einträge in xml und keine Spalte in xlsx

# In[100]:


col_xml = ['fkz', 'db', 'v_thema', 'fi_von/iso8601', 'fi_sumbew/value', 'ver_bez','lp_nr','lp_text','name_st',
          'ort_st','land_st','gem_gemkz_st','name_ze', 'ort_ze', 'land_ze', 'gem_gemkz_ze', 'v_ressort', 
           'v_pt_detail', 'v_forschsp_text','v_prog_text', 'auf_bez_pub', 'auf_bez_pub_quelle', 'auf_bez_pub_en'
          , 'pers_vname_pl', 'pers_name_pl', 'pers_email_pl']
col_xlsx = ['fkz', 'db','v_thema','ver_bez','lp_nr','lp_text','name_st','ort_st','land_st','name_ze', 
            'ort_ze', 'land_ze','v_ressort', 'v_pt_detail','v_forschsp_text', 'v_prog_text', 'auf_bez_pub',
           'auf_bez_pub_quelle', 'auf_bez_pub_en', 'pers_vname_pl', 'pers_name_pl', 'pers_email_pl']
df_xml_part = df[col_xml]
df_xlsx_part = df_xlsx[col_xlsx]
# format und name anpassen
series_start_xlsx = df_xlsx['fi_von.iso8601'].dt.strftime('%Y-%m-%d').rename('fi_von/iso8601')
df_xlsx_part = pd.concat([df_xlsx_part, series_start_xlsx], axis=1)
series_value_xlsx = df_xlsx['fi_sumbew.value'].astype('str').rename('fi_sumbew/value')
df_xlsx_part = pd.concat([df_xlsx_part, series_value_xlsx], axis=1)
series_gemkz_xlsx = df_xlsx['gem_gemkz_st'].astype('str')
df_xlsx_part = pd.concat([df_xlsx_part, series_gemkz_xlsx], axis=1)
series_gemkz_ze_xlsx = df_xlsx['gem_gemkz_ze'].astype('str')
df_xlsx_part = pd.concat([df_xlsx_part, series_gemkz_ze_xlsx], axis=1)


df_fkz_diff = pd.concat([df_xml_part, df_xlsx_part]).drop_duplicates(keep=False)
df_fkz_diff.info()


# In[97]:


df_fkz_diff[['fkz','pers_vname_pl', 'pers_name_pl', 'pers_email_pl']]


# # Zusammenfassung

# ## Abweichung in:
# - fi_ende.iso8601 (Ende-Datum),
# - plz_strasse_st, 
# - ad_str_st, 
# - plz_strasse_ze, 
# - ad_str_ze, pers_pl, 
# - pers_titel_pl
# - pers_vname_pl
# - pers_name_pl
# - pers_email_pl
# 
# 
# ## Keine Daten in
# - auf_bez_pub_quelle_en
# - ohne auf_bez_pub_quelle_en, weil keine Einträge in xml und keine Spalte in xlsx
# 
# ## Unvollständig in
# - auf_bez_pub                             1419 non-null   object        
# - auf_bez_pub_quelle                      1419 non-null   object        
# - auf_bez_pub_en                          1303 non-null   object        
# - auf_bez_pub_en_quelle                   1303 non-null   object  
# - pers_titel_pl                           1305 non-null   object
# - laengengrad_st                          1629 non-null   float64    
# - breitengrad_st                          1629 non-null   float64       
# - Spalte1                                 0 non-null      float64 

# ## Empfehlung: xml-Datei nutzen für die EnArgus-Infos, weil die xlxs (Verteiler) nicht den aktuellsten Stand der EnArgus-Infos enthält
