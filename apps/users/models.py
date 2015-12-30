import os
import hashlib

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from apps.users.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField('Имя',     max_length=30, blank=True, null=True)
    last_name  = models.CharField('Фамилия', max_length=30, blank=True, null=True)

    email       = models.EmailField('E-mail', unique=True)
    date_joined = models.DateTimeField('Дата присоединения', default=timezone.now)

    is_activated = models.BooleanField('E-mail подтверждён', default=True,  help_text='Указывает, что пользователь подтвердил свой e-mail.')
    is_staff     = models.BooleanField('Статус персонала',   default=False, help_text='Указывает, что пользователь имеет доступ к панели администратора.')
    is_active    = models.BooleanField('Активен',            default=True,  help_text='Указывает, что пользователь активен. Используйте вместо удаления аккаунта.')
    moderated    = models.BooleanField('Прошёл модерацию',   default=True,  help_text='Указывает, что пользователь прошёл модерацию.')

    activation_code     = models.CharField('Код активации',     max_length=32, blank=True, null=True)
    reset_password_code = models.CharField('Код сброса пароля', max_length=32, blank=True, null=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def get_short_name(self):
        if self.first_name:
            short_name = self.first_name
        else:
            short_name = self.email.split('@')[0]
        return short_name.strip()

    def get_full_name(self):
        if self.first_name or self.last_name:
            full_name = '%s %s' % (self.first_name, self.last_name)
        else:
            full_name = self.email.split('@')[0]
        return full_name.strip()

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def send_activation_email(self, email=None):

        if email: self.email = email

        self.is_activated = False
        self.activation_code = hashlib.sha256(self.email.encode('utf-8') + os.urandom(256)).hexdigest()[:32]
        self.save()

        subject = 'Добро пожаловать на {0}!'.format(settings.SITE_NAME)
        message = render_to_string('users/emails/activation.html', {'code': self.activation_code, 'site_name': settings.SITE_NAME, 'site_domain': settings.SITE_DOMAIN})

        self.email_user(subject, message, settings.SITE_EMAIL)

    def send_new_password_email(self):

        self.reset_password_code = hashlib.sha256(self.email.encode('utf-8') + os.urandom(256)).hexdigest()[:32]
        self.save()

        subject = 'Сброс пароля на {0}.'.format(settings.SITE_NAME)
        message = render_to_string('users/emails/new_password.html', {'code': self.reset_password_code, 'site_name': settings.SITE_NAME, 'site_domain': settings.SITE_DOMAIN, 'site_email': settings.SITE_EMAIL})

        self.email_user(subject, message, settings.SITE_EMAIL)