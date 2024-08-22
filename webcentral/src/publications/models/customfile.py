__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.db import models
from publications.models import Publication

class CustomFile(models.Model):
	class Meta:
		app_label = 'publications'

	publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
	description = models.CharField(max_length=256)
	file = models.FileField(upload_to='publications/')

	def __unicode__(self):
		return self.description

	def __str__(self):
		return self.description
