# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-27 17:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citydict',
            old_name='city',
            new_name='name',
        ),
    ]