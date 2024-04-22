from django.db import models

# Create your models here.
class CriteriaCatalog(models.Model):
    """Represent a CriteriaCatalog, which holds Tree-Structures of Topics.

    """
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        """Define a String-Representation of a object of type UseCase
        
        This defines, which String is shown in the admin-panel. It should 
        show the `name`-attribute of an `useCase`-Object.
        """
        return self.name


class Topic(models.Model):
    """Represent the Elements inside the hierarchical-structure for each criteriaCatalog.

    """
    heading = models.CharField(max_length=200, null=True, blank=True)
    text = models.CharField(max_length=5000)
    criteriaCatalog = models.ForeignKey("CriteriaCatalog", on_delete=models.CASCADE)
    # useCase = models.OneToOneField("UseCase", on_delete=models.PROTECT)
    parent = models.ForeignKey(
        "Topic", 
        on_delete=models.CASCADE, 
        null=True,
        blank=True,
    )
    imageFilename = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        """Return string representation of an `Topic`-object

        """
        return self.heading