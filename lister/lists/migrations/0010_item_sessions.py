# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-19 03:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('lists', '0009_auto_20160518_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='sessions',
            field=models.ManyToManyField(to='sessions.Session'),
        ),
    ]
