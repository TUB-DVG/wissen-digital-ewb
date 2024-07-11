from tempfile import NamedTemporaryFile
from io import StringIO

from django.test import TestCase
from unittest.mock import patch
from django.core.management import (
    call_command,
    CommandError,
)
import pandas as pd

class TestTools(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         # Perform migrations only once for all tests in this class
#         call_command(
#             "migrate",
#             "tools_over",
#         )
#         call_command(
#             "migrate",
#         )


    @patch("sys.stdout", new_callable=StringIO)
    @patch("sys.stderr", new_callable=StringIO)
    def testCallDataImportForTools(self, mock_stderr, mock_stdout):
        """Check if data-import can be called for data of tools
        data-import-functionality.
        """
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

        with NamedTemporaryFile(prefix="TestTools", suffix=".xlsx", delete=True) as tmp:
            df_german.to_excel(tmp.name, sheet_name="German", index=False)
            df_english.to_excel(tmp.name, sheet_name="English", index=False)
            # with self.assertRaises(CommandError) as context:
            call_command(
                "data_import",
                "Tools",
                "TestTools.xlsx"
            )
                # self.assertIn("Data import into Tools was successful.", mock_stdout.get_value())

