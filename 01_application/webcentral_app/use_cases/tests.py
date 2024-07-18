from random import choice

from django.test import TestCase

from common.views import complexQ

class TestUseCaseFiltering(TestCase):
    """Test if the filtering works as expected

    """

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
        
        randomNumberOfSelections = choice([2, 3, 4])

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
        complexFilterCriterion = complexQ(listOfFilters)
        filteredUseCaseObjs = UseCase.objects.filter(complexFilterCriterion)
        
        # in the queryset `filteredUseCaseObjs` should be elements of all 
        # selected types:
        focusElementsForUseCaseObjs = [(filteredUseCaseObj.focus.all()) for filteredUseCaseObj in filteredUseCaseObjs]
        breakpoint() 

