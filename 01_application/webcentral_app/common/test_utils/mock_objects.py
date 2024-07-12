import pandas as pd

def mock_excel_file():
    data_german = {
        "name": ["Sensormodul"],
        "resources": ["Dokumentation, API"],
        "shortDescription": ["Ein fortschrittliches Sensormodul zur Erfassung von Umweltparametern."],
        "applicationArea": ["Industrie, Umweltüberwachung"],
        "provider": ["Technologie AG"],
        "usage": ["Messung und Überwachung"],
        "lifeCyclePhase": ["Nutzung"],
        "targetGroup": ["Ingenieure, Wissenschaftler"],
        "userInterface": ["Webschnittstelle, App"],
        "userInterfaceNotes": ["Benutzerfreundliche Oberfläche"],
        "programmingLanguages": ["Python, Java"],
        "frameworksLibraries": ["TensorFlow, Keras"],
        "databaseSystem": ["MySQL, MongoDB"],
        "classification": ["Sensorik"],
        "focus": ["Umweltüberwachung"],
        "scale": ["Groß"],
        "lastUpdate": ["2024-07-11"],
        "accessibility": ["Online verfügbar"],
        "license": ["GPLv3"],
        "licenseNotes": ["Freie Nutzung unter GPLv3"],
        "furtherInformation": ["Weitere Details auf der Website"],
        "alternatives": ["Sensormodul B"],
        "specificApplication": ["CO2-Messung"],
        "released": ["Ja"],
        "releasedPlanned": ["Nein"],
        "yearOfRelease": ["2024"],
        "developmentState": ["Produktiv"],
        "technicalStandardsNorms": ["ISO 9001"],
        "technicalStandardsProtocols": ["HTTP, MQTT"],
        "image": ["sensor_image.png"]
    }

    # Create DataFrame for German data
    df_german = pd.DataFrame(data_german)

    # Define the corresponding data in English
    data_english = {
        "name": ["Sensor Module"],
        "resources": ["Documentation, API"],
        "shortDescription": ["An advanced sensor module for capturing environmental parameters."],
        "applicationArea": ["Industry, Environmental Monitoring"],
        "provider": ["Technology Inc."],
        "usage": ["Measurement and Monitoring"],
        "lifeCyclePhase": ["Usage"],
        "targetGroup": ["Engineers, Scientists"],
        "userInterface": ["Web Interface, App"],
        "userInterfaceNotes": ["User-friendly interface"],
        "programmingLanguages": ["Python, Java"],
        "frameworksLibraries": ["TensorFlow, Keras"],
        "databaseSystem": ["MySQL, MongoDB"],
        "classification": ["Sensors"],
        "focus": ["Environmental Monitoring"],
        "scale": ["Large"],
        "lastUpdate": ["2024-07-11"],
        "accessibility": ["Available Online"],
        "license": ["GPLv3"],
        "licenseNotes": ["Free use under GPLv3"],
        "furtherInformation": ["More details on the website"],
        "alternatives": ["Sensor Module B"],
        "specificApplication": ["CO2 Measurement"],
        "released": ["Yes"],
        "releasedPlanned": ["No"],
        "yearOfRelease": ["2024"],
        "developmentState": ["Productive"],
        "technicalStandardsNorms": ["ISO 9001"],
        "technicalStandardsProtocols": ["HTTP, MQTT"],
        "image": ["sensor_image.png"]
    }

    # Create DataFrame for English data
    df_english = pd.DataFrame(data_english)

    return df_german, df_english
