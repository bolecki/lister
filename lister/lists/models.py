from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User


# Create your models here.
@python_2_unicode_compatible
class Lister(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=4)
    list_name = models.CharField(max_length=200)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.list_name


@python_2_unicode_compatible
class Item(models.Model):
    lister = models.ForeignKey(Lister, on_delete=models.CASCADE, default=1)
    item_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.item_text
