from django.db import models
from apps.abs.models import Content

class Test(Content):

    title = models.CharField('Чё тестируем?', max_length=255)


class TestCase(Content):

    url           = models.TextField('Ссылка',            blank=True, null=True)
    case          = models.TextField('Случай',            blank=True, null=True)
    anonymous     = models.TextField('Аноним',            blank=True, null=True)
    not_activated = models.TextField('Не активированный', blank=True, null=True)
    activated     = models.TextField('Активированный',    blank=True, null=True)
    not_active    = models.TextField('Удалённый',         blank=True, null=True)
    not_moderated = models.TextField('Заблокированный',   blank=True, null=True)
    staff         = models.TextField('Админ',             blank=True, null=True)

    test = models.ForeignKey(Test)

    form_params = {'fields': ['url', 'case', 'anonymous', 'not_activated', 'activated', 'not_active', 'not_moderated', 'staff']}

    def __str__(self):
        return str(self.url) + ' ' + str(self.case) if self.url or self.case else str(self.id)