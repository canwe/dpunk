# -*- coding: utf-8 -*-
# Generated by Django 1.9a1 on 2015-10-18 03:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'пост', 'verbose_name_plural': 'посты'},
        ),
        migrations.RemoveField(
            model_name='post',
            name='title1',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title2',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title3',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title4',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title5',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title6',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title7',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title8',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title9',
        ),
        migrations.AddField(
            model_name='post',
            name='anons',
            field=models.TextField(default=123, help_text='Будет отображаться в лента материалов', verbose_name='Анонс'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(help_text='Будет отображаться только на странице материала', verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
    ]
