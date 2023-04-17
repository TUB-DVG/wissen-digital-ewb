"""

"""

import unittest
import pdb

from django.test import TestCase
from django.core import management

from project_listing.models import Teilprojekt
from project_listing.management.commands.data_import import Command

class checkDifferencesInDatabase(TestCase):
    """
    
    """

    def testImportSimpleDataset(self):
        """This method tests, if a single Dataset can be loaded into the 
        database and if the database-tuple represents the data right.
        For that, django automatically sets up a empty test-database, 
        which is filled with one dataset.
        
        """
        strOfColumnNames = "FKZ;Laufzeitbeginn;Laufzeitende;Datenbank;Thema;Foerdersumme_EUR;Verbundbezeichung;Leistungsplan_Sys_Nr;Leistungsplan_Sys_Text;Name_ZWE;PLZ_ZWE;Ort_ZWE;Adress_ZWE;Land_ZWE;Bundesministerium;Projekttraeger;Forschungsprogramm;Foerderprogramm;Kurzbeschreibung_de;Kurzbeschreibung_en;Person_pl;Titel_pl;Vorname_pl;Name_pl;Email_pl;Name_AS;PLZ_AS;Ort_AS;Adress_AS;Land_AS"
        strOfDataset = "03EWR008J;2021-04-01;2026-03-31;PROFI;'Reallabor: Reallabor_GWP - Großwärmepumpen in Fernwärmenetzen - Installation, Betrieb, Monitoring und Systemeinbindung; Teilvorhaben: Stadtwerke Rosenheim (FuE)';101261.0;Reallabor: Reallabor_GWP;EA2150;Wärmetransport und -verteilung;Stadtwerke Rosenheim GmbH & Co. KG;83022;Rosenheim;Bayerstr. 5;Bayern;BMWK;Forschungszentrum Jülich GmbH;Energietechnologien (BMWi);Energie;Großwärmepumpen (GWP) in Fernwärmenetzen haben das Potenzial, treibhausgasfreie Wärme in Ballungsräumen kostengünstig bereitzustellen. Das geplante Verbundvorhaben soll die wissenschaftlichen Grundlagen legen, um dieses Potenzial für das deutsche Energiesystem ausschöpfen zu können. 2020 sind in Deutschland noch keine GWP in Betrieb. Zentrales Ziel der Forschungsarbeiten ist daher die Beantwortung technischer, ökologischer und wirtschaftlicher Fragestellungen hinsichtlich der Integration von GWP in deutsche Fernwärmenetze. Es ist dabei geplant unter anderem Teillastverhalten, Regelung, Einsatzdauern sowie Wege zur Treibhausgasneutralität im realen Betrieb zu untersuchen. Als Voraussetzung für eine breite Marktdurchdringung durch GWP soll ein Ausblick zu einer möglichen Anpassung des geltenden Rechtsrahmens die vorhergehenden Untersuchungen ergänzen. Um die Projektziele zu erreichen, werden an fünf bestehenden Fernwärmeerzeugungsstandorten GWP mit einer thermischen Leistung zwischen 1,12 bis 22 MW installiert. In einem dreijährigen Forschungs- und Entwicklungsbetrieb sollen im nächsten Schritt zeitlich hoch aufgelöste Realdaten erfasst werden. Diese werden mit Hilfe von Energiesystemmodellen und -analysen wissenschaftlich ausgewertet. Eine abschließende Übertragung der Ergebnisse auf Deutschland soll zeigen, inwiefern GWP in Fernwärmenetzen am besten zur Sektorkopplung und Treibhausgasreduktion beitragen können. Das Verbundvorhaben soll die Fernwärmebranche und den Gesetzgeber darin unterstützen, das Potenzial von GWP für systemdienliche, treibhausgasfreie Fernwärme in Deutschland auszuschöpfen.;Large-scale heat pumps (LHP) in district heating networks have the potential to provide heat free of greenhouse gases at low cost in urban areas. The planned joint project is intended to lay the scientific foundations for exploiting this potential for the German energy system. In 2020, no LHPs are in operation in Germany. The central aim of this research project is therefore to answer technical, ecological and economic questions regarding the integration of LHP into German district heating networks. It is planned to investigate, among other things, partial load behaviour, regulation, operating times and ways to achieve greenhouse gas neutrality in real operation. As a prerequisite for a broad market penetration by LHP, an outlook on a possible adaptation of the current legal framework will complement the previous studies. To achieve the project objectives, LHPs with a thermal capacity between 1.12 and 22 MW will be installed at five existing district heating generation sites. A three-year research and development operation phase is targeted at collecting real data with high temporal resolution. This data will be scientifically evaluated with the help of energy system models and analyses. Finally, a transfer of the results to Germany will show how LHP in district heating networks can best contribute to sector coupling and greenhouse gas reduction. The joint project aims to support the district heating sector and the legislator in exploiting the potential of LHP for systemically useful, greenhouse gas-free district heating in Germany.;Sebastian Hochmuth;;Sebastian;Hochmuth;sebastian.hochmuth@swro.de;Stadtwerke Rosenheim GmbH & Co. KG;83022;Rosenheim;Bayerstr. 5;Bayern"
        testCSVFileName = "enargus_oneDatasetTest.csv"
        with open(testCSVFileName, "w") as testfile:
            testfile.write(strOfColumnNames+'\n')
            testfile.write(strOfDataset)
        
        pdb.set_trace()

        # do a migration to make it possible to import the data:
        management.call_command('migrate')

        # load the dataset into the empty database:
        management.call_command('data_import', testCSVFileName)

        # the test
        self.assertTrue(len(Teilprojekt.objects.all()) == 1)

        dataImportCommand = Command()
        header, data = dataImportCommand.readCSV(testCSVFileName)
        pdb.set_trace()

        # at first at a dataset to the empty database, which will be modified later:
        management.call_command('data_import_update', "../../02_work_doc/01_daten/01_prePro/testOneDataSet.csv")
        management.call_command('data_import_update', "../../02_work_doc/01_daten/01_prePro/testModifiedDataSet.csv")

        # with open("dbDiffs.csv", "a") as f:
        #     pdb.set_trace()



# if __name__ == "__main__":
#     unittest.main()