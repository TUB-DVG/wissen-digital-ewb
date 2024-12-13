__license__ = "MIT License <http://www.opensource.org/licenses/mit-license.php>"
__author__ = "Lucas Theis <lucas@theis.io>"
__docformat__ = "epytext"

from django.contrib import admin

from common.admin import HistoryAdmin
from publications.models import Type, List, Publication, History
from .publicationadmin import PublicationAdmin
from .typeadmin import TypeAdmin
from .listadmin import ListAdmin
from .orderedmodeladmin import OrderedModelAdmin


class HistoryAdminApp(HistoryAdmin):
    """ """

    modelInstance = Publication
    historyModelInstance = History
    attributeName = "title"


admin.site.register(History, HistoryAdminApp)
admin.site.register(Type, TypeAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(Publication, PublicationAdmin)
