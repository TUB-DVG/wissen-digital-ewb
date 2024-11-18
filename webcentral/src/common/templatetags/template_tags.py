"""This module defines a custom template tag, which can be used in the
django HTML-templates.

"""

from django import template

register = template.Library()


@register.filter
def get_attribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    return getattr(value, arg)

@register.filter
def get_m2m_or_attr(djangoModelObj, argStr):
    """Get a attribute from a django-model and return the value.

    The argument can also encode a table connection with the __ syntax.
    E.g. `license__openSourceStatus` means the attribute `openSourceStatus`
    in the table, which is connected through the `license` attribute.
    
    """

    if "__" in argStr:
        try:
            m2mAttr, attributeInReferencedTable = argStr.split("__")
            if isinstance(m2mAttr, str) and isinstance(attributeInReferencedTable, str):
                returnStr = ""
                for connectedObj in getattr(djangoModelObj, m2mAttr).all():
                    returnStr += getattr(connectedObj, attributeInReferencedTable) + ", "
                return returnStr[:-1]
            else:
                raise TypeError("Only one __ should be present in the argument string.")
        except:
            pass

    else:
        return get_attribute(djangoModelObj, argStr)

