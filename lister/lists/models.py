from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
@python_2_unicode_compatible
class Lister(models.Model):
    list_name = models.CharField(max_length=200)

    def __str__(self):
        return self.list_name

@python_2_unicode_compatible
class Item(models.Model):
    lister = models.ForeignKey(Lister, on_delete=models.CASCADE, default=1)
    item_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.item_text

