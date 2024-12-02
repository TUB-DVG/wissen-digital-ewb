from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import RequestFactory

# from .admin import HistoryAdminApp

User = get_user_model()


class AbstractTestUpdate(TestCase):
    """Abstract Test class for the TestUpdate-class, which is inheried from in all apps
    to test the Update process

    """

    def setUp(self):
        """setUp method for all methods of `DbDiffAdminTest`"""

        self.site = AdminSite()
        self.historyAdmin = self.historyAdminAppCls(
            self.historyModelCls, self.site
        )

        # Create a test user and request factory
        self.user = User.objects.create_superuser(
            username="admin", password="password", email="admin@example.com"
        )
        self.factory = RequestFactory()
