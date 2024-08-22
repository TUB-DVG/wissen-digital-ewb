'''
    File name: pre_toolsProjects.py
    Author: Siling Chen
    Date created: 2023-10-30
    Date last modified:
    Python Version: 3.9
    Description: This file is a script for preprocessing the Fragenbogen 
        - search for application of tools that exist in our databank to projects
'''
import os
import pandas as pd
import numpy as np

# transfer Fragenbogen 1 to toolsFileName 
''' Note: due to typo or other naming issues, application for the following tools were 
            filled in after manual search
            R; PostgresSQL; STAR CCM+, Grasshopper, Ansys Fluid, T*sol 

'''
projectsFileName =  '/Users/silingchen/Downloads/Tools/data_finished_Text_v09.xlsx'
toolsFileName = '/Users/silingchen/Downloads/Tools/2023_10_23_EWB_Tools_Uebersicht_3110.xlsx'

toolColumn = 'DI03_01' # Welche digitalen Anwendungen nutzen  oder entwickeln Sie im Projekt
projectReferenceNumberColumn = 'ZU01_01' # Förderkennzeichen

projectInfo = pd.read_excel(projectsFileName, index_col=0)
projectApplications = projectInfo[[toolColumn]]

tools = pd.read_excel(toolsFileName, index_col=0)

allToolProjectReferenceNumbers = []
for tool in tools.index:
    toolProjectReferenceNumbers = []
    for pp, projectApplicationText in enumerate(list(projectApplications[toolColumn])):
        if type(projectApplicationText) == str:
            if tool.upper() in projectApplicationText.upper():
                toolProjectReferenceNumbers.append(projectInfo[projectReferenceNumberColumn].loc[pp])
            
    allToolProjectReferenceNumbers.append(toolProjectReferenceNumbers)   
tools['specificApplication'] = allToolProjectReferenceNumbers
tools.to_excel(toolsFileName.replace('.xlsx', '_specificApplication.xlsx'))
# followed by manual control and edits, as noted above

########
# transfer Fragenbogen 2 to toolsFileName 
''' Note: due to naming issues, application for the following tools is 
            filled in after manual search
            R 

'''
projectsFileName =  '/Users/silingchen/Downloads/Tools/data_EWB2023-M2_2023-06-15_09-16 (1).xlsx' 
toolsFileName = '/Users/silingchen/Downloads/Tools/2023_10_23_EWB_Tools_Uebersicht_3110.xlsx'

toolColumns = ['D003x01', 'D003x02', 'D003x03']
projectReferenceNumberColumn = 'SERIAL' # Förderkennzeichen

toolColumn = toolColumns[0]
projectInfo = pd.read_excel(projectsFileName, index_col=0)


tools = pd.read_excel(toolsFileName, index_col=0)

allToolProjectReferenceNumbers = []
for tool in tools.index:
    toolProjectReferenceNumbers = []
    for toolColumn in toolColumns:
        projectApplications = projectInfo[[toolColumn]]
        for pp, projectApplicationText in enumerate(list(projectApplications[toolColumn])):
            if type(projectApplicationText) == str:
                if tool.upper() in projectApplicationText.upper():
                    toolProjectReferenceNumbers.append(projectInfo[projectReferenceNumberColumn].iloc[pp])
    allToolProjectReferenceNumbers.append(toolProjectReferenceNumbers)   

tools['specificApplication_'] = allToolProjectReferenceNumbers
tools.to_excel(toolsFileName.replace('.xlsx', '_specificApplication_.xlsx'))
# followed by manual control and edits, and merging of the above two generated columns 