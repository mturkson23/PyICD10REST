from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    """
    ICD10 codes category
    """
    short_code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)


class Code(models.Model):
    """
    ICD10 codes object
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    diagnosis_code = models.CharField(max_length=50, unique=True)
    short_description = models.CharField(max_length=255)
    full_description = models.CharField(max_length=255, )
