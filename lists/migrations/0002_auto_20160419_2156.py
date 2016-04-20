# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 01:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='item',
            old_name='list_text',
            new_name='item_text',
        ),
        migrations.AddField(
            model_name='item',
            name='lister',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lists.Lister'),
        ),
    ]
