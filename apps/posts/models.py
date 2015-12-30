# -*- coding: utf-8 -*-

from django.db import models

from apps.abs.models import UserContent

class Post(UserContent):

    title = models.CharField('Заголовок', max_length=255)

    anons = models.TextField('Анонс', help_text='Будет отображаться в ленте материалов в качестве анонса, и на странице материала в качестве вступления')
    text  = models.TextField('Текст', help_text='Будет отображаться только на странице материала', blank=True, null=True)

    form_params = {'fields': ['title', 'anons', 'text', 'published']}

    class Meta:
        verbose_name = u'статья'
        verbose_name_plural = u'статьи'
        verbose_name_rod = u'статью'
        ordering = ['-date_created']
