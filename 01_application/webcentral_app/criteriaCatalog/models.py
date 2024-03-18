from django.db import models

# Create your models here.
class UseCase(models.Model):
    """Represent the root of the hierachy-structure

    """
    name = models.CharField(max_length=100)
    text = models.CharField(max_length=500, blank=True)

    def __str__(self):
        """Define a String-Representation of a object of type UseCase
        
        This defines, which String is shown in the admin-panel. It should 
        show the `name`-attribute of an `useCase`-Object.
        """
        return self.name




# class Parent(models.Model):
#     """Represent the hierarchial structure of the data

#     """
#     parent = models.OneToOneField(SubTopic, on_delete=models.PROTECT)

class Topic(models.Model):
    """Represent the sub-topics in the hierarchical-structure.

    """
    text = models.CharField(max_length=200)
    useCase = models.ForeignKey("UseCase", on_delete=models.CASCADE)
    # useCase = models.OneToOneField("UseCase", on_delete=models.PROTECT)
    parent = models.ForeignKey(
        "Topic", 
        on_delete=models.PROTECT, 
        null=True,
        blank=True,
    )

    def __str__(self):
        """Return string representation of an `Topic`-object

        """
        return self.text