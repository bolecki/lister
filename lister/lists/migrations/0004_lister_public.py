# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_lister_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='lister',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
