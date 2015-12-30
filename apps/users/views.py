# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import modelform_factory
from django.core.urlresolvers import reverse

from apps.users.forms import SignupForm, LoginForm, PasswordResetForm, ChangeEmailForm, PasswordChangeForm, SetPasswordForm, UserEditForm, BasePasswordForm
from apps.users.utils import auth
from apps.users.models import User
from apps.users.decorators import logout_required

def user_detail(request, user_id=None):

    if not user_id and request.user.is_authenticated():
        return redirect(reverse('user_detail', args=(request.user.id,)))
    elif not user_id:
        return redirect(reverse('user_login'))

    user = get_object_or_404(User, id=user_id)

    params = {}

    if request.user != user and not request.user.is_staff:
        params['published'] = True
        params['moderated'] = True

    return render(request, 'users/user_detail.html', {'user_object': user, 'user_posts': user.post_set.filter(**params)})

@logout_required
def user_signup(request):
    form = SignupForm(request.POST or None)
    if request.POST and form.is_valid():
        del form.cleaned_data['password2']
        User.objects.create_user(**form.cleaned_data)
        user = auth(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        user.send_activation_email()
        return redirect(reverse('user_detail'))
    return render(request, 'users/user_signup.html', {'form': form})

@logout_required
def user_login(request):

    form = LoginForm(request.POST or None)
    redirect_to = request.GET.get('next', '')

    if request.POST and form.is_valid():
        auth(request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
        redirect_to = request.POST.get('next', '')
        return redirect(redirect_to) if redirect_to else redirect(reverse('user_detail'))

    return render(request, 'users/user_login.html', {'form': form, 'next': redirect_to})

@login_required
def user_edit(request):

    user = get_object_or_404(User, id=request.user.id)
    form = UserEditForm(request.POST or None, request.FILES or None, instance=user)
    redirect_to = request.GET.get('next', '')

    if request.POST and form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, u'Информация обновлена')
        redirect_to = request.POST.get('next', '')
        return redirect(redirect_to) if redirect_to else redirect(reverse('user_edit'))

    return render(request, 'users/user_edit.html', {'form': form, 'user_object': request.user, 'next': redirect_to})

@login_required
def user_send_activation(request):
    if request.user.is_activated:
        messages.add_message(request, messages.INFO, u'Пользователь уже активирован')
    else:
        request.user.send_activation_email()
        messages.add_message(request, messages.INFO, u'Вам выслано повторное письмо активации на {0} для подтверждения e-mail'.format(request.user.email))
    return redirect(request.META.get('HTTP_REFERER'))

def user_activation(request, code):

    user = User.objects.check_code('activation_code', code)

    if user:
        User.objects.activate(code)
        messages.add_message(request, messages.SUCCESS, u'Спасибо, Ваш E-mail подтверждён')
    else:
        messages.add_message(request, messages.ERROR, u'Ключ не верен либо устарел')

    if request.user.is_authenticated():
        return redirect(reverse('user_detail'))
    else:
        return redirect(reverse('home'))

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('home'))

@login_required
def user_change_email(request):
    user = get_object_or_404(User, id=request.user.id)
    form = ChangeEmailForm(request.POST or None, request.FILES or None, instance=user)
    if request.POST and form.is_valid():
        request.user.send_activation_email(form.cleaned_data['email'])
    return render(request, 'users/user_change_email.html', {'form': form})

@logout_required
def user_forgot_password(request):
    form = PasswordResetForm(request.POST or None)
    if request.POST and form.is_valid():
        get_object_or_404(User, email=form.cleaned_data['email']).send_new_password_email()
        messages.add_message(request, messages.INFO, u'Ссылка для смены пароля выслана на {0}'.format(form.cleaned_data['email']))
    return render(request, 'users/user_forgot_password.html', {'form': form})

def user_new_password(request, code):
    user_to_reset = User.objects.check_code('reset_password_code', code)
    form = SetPasswordForm(user=user_to_reset, data=request.POST or None)
    if user_to_reset:
        if request.POST and form.is_valid():
            form.save()
            User.objects.set_new_password(code)
            add_message = u', а пользователь активирован' if not user_to_reset.is_activated else u''
            messages.add_message(request, messages.SUCCESS, u'Пароль успешно изменён' + add_message)
            return redirect(reverse('user_detail'))
        return render(request, 'users/user_new_password.html', {'form': form, 'code': code, 'user_to_reset': user_to_reset})
    else:
        messages.add_message(request, messages.ERROR, u'Ключ не верен либо устарел')
        return redirect(reverse('home'))


@login_required
def user_change_password(request):
    form = PasswordChangeForm(user=request.user, data=request.POST or None)
    if request.POST and form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, u'Пароль успешно изменён')
        return redirect(reverse('user_detail'))
    return render(request, 'users/user_change_password.html', {'form': form,})

@login_required
def user_delete(request):
    user = get_object_or_404(User, id=request.user.id)
    form = modelform_factory(User, fields=[])(data=request.POST or None)
    if request.POST and form.is_valid():
        user.is_active = False if user.is_active else True
        user.save()
        message = u'Аккаунт восстановлен' if user.is_active else u'Аккаунт поставлен в очередь на удаление'
        message_type = messages.SUCCESS if user.is_active else messages.INFO
        messages.add_message(request, message_type, message)
        if user.is_active:
            return redirect(reverse('user_detail'))
        else:
            return redirect(reverse('user_delete'))
    return render(request, 'users/user_delete.html', {'form': form,})