# -*- coding: utf-8 -*-
# Generated by Django 1.9a1 on 2015-10-18 01:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('published', models.BooleanField(default=True, verbose_name='Опубликован')),
                ('moderated', models.BooleanField(default=True, verbose_name='Прошёл модерацию')),
                ('title', models.CharField(max_length=255)),
                ('title1', models.CharField(blank=True, max_length=255, null=True)),
                ('title2', models.CharField(blank=True, max_length=255, null=True)),
                ('title3', models.CharField(blank=True, max_length=255, null=True)),
                ('title4', models.CharField(blank=True, max_length=255, null=True)),
                ('title5', models.CharField(blank=True, max_length=255, null=True)),
                ('title6', models.CharField(blank=True, max_length=255, null=True)),
                ('title7', models.CharField(blank=True, max_length=255, null=True)),
                ('title8', models.CharField(blank=True, max_length=255, null=True)),
                ('title9', models.CharField(blank=True, max_length=255, null=True)),
                ('text', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'резюме',
                'verbose_name_plural': 'резюме',
            },
        ),
    ]