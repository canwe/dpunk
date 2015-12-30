# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone

class Content(models.Model):

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self, 'title'):
            title = self.title
        elif hasattr(self, 'date'):
            title = self.date
        elif hasattr(self, 'id'):
            title = self.id
        else:
            title = ''
        return str(title)

    def meta(self):
        return self._meta

    def app_label(self):
        return self._meta.app_label.lower()

    def object_name(self):
        return self._meta.object_name.lower()

    def app_object_name(self):
        return self.app_label() + '_' + self.object_name()

class UserContent(Content):

    user = models.ForeignKey('users.User')
    date_created = models.DateTimeField(u'Дата создания', default=timezone.now)
    published = models.BooleanField(verbose_name=u'Опубликовано', default=True)
    moderated = models.BooleanField(verbose_name=u'Прошёл модерацию', default=True)

    def published_moderated(self):
        return True if self.published and self.moderated else False

    class Meta:
        abstract = True