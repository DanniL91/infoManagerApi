from django.db import models

# Create your models here.
class Person(models.Model):
    class Meta:
        unique_together = (('documentType', 'documentNumber'),)

    documentType = models.CharField(max_length=4)
    documentNumber = models.IntegerField(null = False)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    second_name = models.CharField(max_length=50, null=True, blank=True)
    lastName = models.CharField(max_length=100, null=False, blank=False)
    hobbie = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.first_name