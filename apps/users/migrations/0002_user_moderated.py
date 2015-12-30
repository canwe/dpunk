# -*- coding: utf-8 -*-
# Generated by Django 1.9a1 on 2015-11-01 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='moderated',
            field=models.BooleanField(default=True, help_text='Указывает, что пользователь прошёл модерацию.', verbose_name='Прошёл модерацию'),
        ),
    ]