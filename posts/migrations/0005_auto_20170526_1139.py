# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20170526_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, to='posts.Tag'),
        ),
    ]
