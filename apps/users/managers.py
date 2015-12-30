# -*- coding: utf-8 -*-

import string, re

from django.utils import timezone
from django.contrib.auth.models import BaseUserManager

ACTIVATION_CODE_REGEX = '[' + string.hexdigits + ']{32}'

class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

    def check_code(self, field, code):
        user_obj = None
        if re.match(ACTIVATION_CODE_REGEX, code):
            user = self.filter(**{field:code})
            if user.exists():
                user_obj = user[0]
        return user_obj

    def activate(self, activation_code):
        user = self.check_code('activation_code', activation_code)
        if user:
            user.activation_code, user.is_activated = None, True
            user.save()
        return user

    def set_new_password(self, reset_password_code):
        user = self.check_code('reset_password_code', reset_password_code)
        if user:
            user.activation_code, user.reset_password_code, user.is_activated = None, None, True
            user.save()
        return user
