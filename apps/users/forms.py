# -*- coding: utf-8 -*-

from collections import OrderedDict

from django import forms
from django.core import validators
from django.contrib.auth import authenticate

from apps.users.models import User

class BasePasswordForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput, label=u'Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label=u'Пароль ещё раз')

    def clean_password2(self):
        password1, password2 = self.cleaned_data.get('password'), self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'Пароли не совпадают')
        return password2

class SignupForm(BasePasswordForm):
    email = forms.CharField(label=u'E-mail', validators=[validators.EmailValidator(message=u'Введите корректный E-mail адрес')])

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields = OrderedDict((k, self.fields[k]) for k in ['email', 'password', 'password2'])

    def clean_email(self):
        user = User.objects.filter(email=self.cleaned_data['email'])
        if user.exists():
            raise forms.ValidationError(u'Указанный E-mail уже используется')
        return self.cleaned_data['email']

class LoginForm(forms.Form):

    email    = forms.CharField(label=u'E-mail', validators=[validators.EmailValidator(message=u'Введите корректный E-mail адрес')])
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput)

    def clean_email(self):
        user = User.objects.filter(email=self.cleaned_data['email'])
        if not user.exists():
            raise forms.ValidationError(u'Пользователь с таким e-mail не зарегистрирован')
        return self.cleaned_data['email']

    def clean_password(self):
        if not authenticate(email=self.cleaned_data.get('email'), password=self.cleaned_data.get('password')):
            raise forms.ValidationError(u'Не верный пароль')
        return self.cleaned_data['password']

class PasswordResetForm(forms.Form):

    email = forms.CharField(label=u'E-mail', validators=[validators.EmailValidator(message=u'Введите корректный E-mail адрес')])

    def clean_email(self):
        user = User.objects.filter(email=self.cleaned_data['email'])
        if not user.exists():
            raise forms.ValidationError(u'Пользователя с указанным e-mail не существует')
        return self.cleaned_data['email']

class ChangeEmailForm(forms.ModelForm):

    email = forms.CharField(label=u'Новый E-mail', validators=[validators.EmailValidator(message=u'Введите корректный E-mail адрес')])

    def clean_email(self):
        user = User.objects.filter(email=self.cleaned_data['email'])
        if user.exists():
            raise forms.ValidationError(u'Указанный Вами e-mail уже используется')
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['email']

class SetPasswordForm(BasePasswordForm):

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def save(self):
        self.user.set_password(self.cleaned_data['password'])
        self.user.save()
        return self.user

class PasswordChangeForm(SetPasswordForm):

    current_password = forms.CharField(label=u'Текущий пароль', widget=forms.PasswordInput)

    def clean_current_password(self):
        current_password = self.cleaned_data["current_password"]
        if not self.user.check_password(current_password):
            raise forms.ValidationError(u'Текущий пароль не верен')
        return current_password

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields = OrderedDict((k, self.fields[k]) for k in ['current_password', 'password', 'password2'])
        self.fields['password'].label  = u'Новый пароль'
        self.fields['password2'].label = u'Новый пароль ещё раз'

class UserEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required, self.fields['last_name'].required = True, True

    class Meta:
        model = User
        fields = ['first_name', 'last_name']