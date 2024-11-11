from django import template
from django.db import models

register = template.Library()


# @register.filter(name="getObjAttr")
# def getObjAttr(obj, attr):
#     if isinstance(obj._meta.get_field(attr), models.ManyToManyField):
#         return obj.getManyToManyWithTranslation(attr)
#
#     return getattr(obj, attr)
#
register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
