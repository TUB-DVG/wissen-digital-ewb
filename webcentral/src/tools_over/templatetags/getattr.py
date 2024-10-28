from django import template

register = template.Library()

@register.filter(name="getObjAttr")
def getObjAttr(obj, attr):
    """Removes all values of arg from the given string"""
    return getattr(obj, attr)
