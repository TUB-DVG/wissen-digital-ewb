from django.test import TestCase

from .models import (
    Category,   
    Component,
    ComponentClass,
)

# Create your tests here.
class TestRounding(TestCase):
    """This testclass tests the rounding functionality when 
    FloatFields are displayed.

    """
    def testFindLastDecimalPlaces(self):
        """

        """
        categoryObj = Category.objects.create(
            category="testCategory",
        )
        
        componentClassObj = ComponentClass.objects.create(
            componentClass="TestComponentClass",
        )

        exampleFloatOne = 1.00020
        componentObj = Component.objects.create(
            category=categoryObj,
            component=componentClassObj,
        )

        returnValueFloatOne = componentObj._findLastDecimalPlaces(str(exampleFloatOne))
        self.assertEqual(returnValueFloatOne, 5)
    
        exampleFloatTwo = 1.00021
        returnValueFloatTwo = componentObj._findLastDecimalPlaces(str(exampleFloatTwo))
        self.assertEqual(returnValueFloatTwo, 5)

        exampleFloatThree = 1.8396
        returnValueFloatThree = componentObj._findLastDecimalPlaces(str(exampleFloatThree))
        self.assertEqual(returnValueFloatThree, 2)

        exampleFloatFour = 10
        returnValueFloatFour = componentObj._findLastDecimalPlaces(str(exampleFloatFour))
        self.assertEqual(returnValueFloatFour, 0)

