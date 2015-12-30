# -*- coding: utf-8 -*-

from functools import wraps

from django.core.urlresolvers import reverse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404

from apps.users.models import User

def name_required(func):
    def closure(request, *args, **kwargs):
        if not request.user.first_name or not request.user.last_name:
            messages.add_message(request, messages.INFO, u'Пожалуйста, сначала представьтесь')
            return redirect(reverse('user_edit') + '?next=' + request.path)
        else:
            return func(request, *args, **kwargs)
    return wraps(func)(closure)

def logout_required(func):
    def closure(request, *args, **kwargs):
        if request.user.is_authenticated():
            messages.add_message(request, messages.INFO, u'Вы авторизованы')
            return redirect('user_detail')
        else:
            return func(request, *args, **kwargs)
    return wraps(func)(closure)

def activated_required(func):
    u"""Пользователь должен быть активирован"""
    def closure(request, *args, **kwargs):
        if not request.user.is_activated:
            messages.add_message(request, messages.INFO, u'Пожалуйста, сначала подтвердите, что {0} действительно Ваш E-mail адрес'.format(request.user.email), extra_tags='safe')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return func(request, *args, **kwargs)
    return wraps(func)(closure)

def owner_required(model=None):
    def decorator(func):
        def closure(request, *args, **kwargs):
            Model = kwargs['model'] if 'model' in kwargs else model
            if not request.user.is_staff and 'object_id' in kwargs and get_object_or_404(Model, id=kwargs['object_id']).user != request.user:
                raise Http404
            else:
                return func(request, *args, **kwargs)
        return wraps(func)(closure)
    return decorator
