from random import choice

from django.test import TestCase
from django.core.management import call_command

from common.views import createQ
from tools_over.models import Focus
from use_cases.models import UseCase

class TestUseCaseFiltering(TestCase):
    """Test if the filtering works as expected

    """

    def setUp(self):
        """Is executed before every test.


        """
        call_command("data_import", "use_cases", "../../02_work_doc/01_daten/14_use_cases/20240423_daten_use_cases.xlsx", ".")

        technicalFocusObj = Focus.objects.filter(focus="technisch")[0]
        technicalFocusObj.focus_en = "technical"
        technicalFocusObj.save()
        operationalFocusObj = Focus.objects.filter(focus="betrieblich")[0]
        operationalFocusObj.focus_en = "operational"
        operationalFocusObj.save()
        ecologicalFocusObj = Focus.objects.filter(focus="ökologisch")[0]
        ecologicalFocusObj.focus_en = "ecological"
        ecologicalFocusObj.save()
        legalFocusObj = Focus.objects.filter(focus="rechtlich")[0]
        legalFocusObj.focus_en = "legal"
        legalFocusObj.save()



    def testMultipleFocusElementsSelected(self):
        """Test if `UseCase`-objects of all selected 
        types are returned.

        """
        
        possibleUseCases = [
            "operational", 
            "ecological", 
            "legal", 
            "technical",
        ]

        # select 2-4 elements:
        selectedFocusElements = []
        
        randomNumberOfSelections = choice(
            [
                2, 
                3, 
                4,
            ]
        )

        if randomNumberOfSelections == 4:
            selectedFocusElements = possibleUseCases
        else:
            for index in range(randomNumberOfSelections):
                selectedFocus = choice(possibleUseCases)
                possibleUseCases.remove(selectedFocus)
                selectedFocusElements.append(selectedFocus)
        
        listOfFilters = [
            {
                "filterValues": selectedFocusElements,
                "filterName": "focus__focus__icontains",
                "filterNameEn": "focus__focus_en__icontains",
            },
            {
                "filterValues": [],
                "filterName": "degreeOfDetail__icontains",
            },
            {
                "filterValues": [],
                "filterName": "effectEvaluation__icontains",
            },
        ]
        complexFilterCriterion = createQ(listOfFilters)
        filteredUseCaseObjs = UseCase.objects.filter(complexFilterCriterion)
        
        # in the queryset `filteredUseCaseObjs` should be elements of all 
        # selected types:
        focusElementsForUseCaseObjs = [(filteredUseCaseObj.focus.all()) for filteredUseCaseObj in filteredUseCaseObjs]
        sortUseCasesIntoFocusBuckets = {}
        for focusStr in selectedFocusElements:
            sortUseCasesIntoFocusBuckets[focusStr] = []
            for filteredUseCaseObj in filteredUseCaseObjs:
                for currentFocus in filteredUseCaseObj.focus.all():
                    if focusStr in currentFocus.focus or focusStr in currentFocus.focus_en:
                        sortUseCasesIntoFocusBuckets[focusStr].append(filteredUseCaseObj)

        for useCaseBucket in list(sortUseCasesIntoFocusBuckets.keys()):
            self.assertGreater(len(useCaseBucket), 0)

    def testMultipleSelectedUseElements(self):
        """Test the behaviour if multiple use-elements are selected.

        """
        
        listOfdegreeOfDetailElements = list(set([useCaseObj.degreeOfDetail for useCaseObj in UseCase.objects.all()]))

        numberOfChoices = choice([2, 3, 4])
        chosenUseElements = []
        for index in range(numberOfChoices):
            randomChoice = choice(listOfdegreeOfDetailElements)
            listOfdegreeOfDetailElements.remove(randomChoice)
            chosenUseElements.append(randomChoice)

        listOfFilters = [
            {
                "filterValues": [],
                "filterName": "focus__focus__icontains",
                "filterNameEn": "focus__focus_en__icontains",
            },
            {
                "filterValues": chosenUseElements,
                "filterName": "degreeOfDetail__icontains",
            },
            {
                "filterValues": [],
                "filterName": "effectEvaluation__icontains",
            },
        ]
        complexFilter = createQ(listOfFilters)
        
        filteredUseCaseObj = UseCase.objects.filter(complexFilter)
        
        for currentChosenElement in chosenUseElements:
            if len(UseCase.objects.filter(degreeOfDetail__icontains=currentChosenElement)) > 0:
                self.assertGreater(len(filteredUseCaseObj.filter(degreeOfDetail__icontains=currentChosenElement)), 0)



 
