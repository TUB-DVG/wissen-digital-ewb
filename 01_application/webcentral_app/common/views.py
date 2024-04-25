from django.shortcuts import render

from tools_over.models import Focus

def getFocusObjectFromGetRequest(focusStr) -> Focus:
    """Get the focus object from the get request.
    
    """
    englishFocus = Focus.objects.filter(focus_en=focusStr)
    germanFocus = Focus.objects.filter(focus_de=focusStr)
    focusElements = englishFocus | germanFocus
    if len(focusElements) > 0:
        return focusElements[0]
    return None

def getFocusNameIndependentOfLanguage(focusStr: str, focusObj: Focus) -> str:
    """Return the focus name, which is used inside the css-classname
    
    """
    if focusStr is None or focusStr == "":
        focusName = "neutral"
    else:
        focusName = focusObj.focus_en
    return focusName