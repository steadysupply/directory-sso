# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-02-08 16:33
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20161130_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='utm',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=[]),
        ),
    ]
