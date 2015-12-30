# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect, render
from django.forms.models import modelform_factory
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from apps.users.decorators import owner_required, activated_required, name_required

def post_detail(request, model, object_id=None, object_slug=None, template='posts/post_detail.html'):
    params = {'slug': object_slug} if object_slug else {'id': object_id}
    return render(request, template, {
        'object': get_object_or_404(model, **params),
    })

@login_required
@activated_required
@owner_required(model=None)
@name_required
def post_form(request, model, object_id=None, template='posts/post_form.html', form=None):
    obj = get_object_or_404(model, id=object_id) if object_id else None
    form = form if form else modelform_factory(model, **model.form_params)(data=request.POST or None, files=request.FILES or None, instance=obj)
    if request.POST and form.is_valid():
        new_obj = form.save(commit=False)
        new_obj.user = request.user
        new_obj.save()
        form.save_m2m()
        messages.add_message(request, messages.SUCCESS, u'Сохранено')
        return redirect(reverse(new_obj.object_name() + '_detail', args=(new_obj.id,)))
    return render(request, template, {
        'object': obj,
        'form': form,
    })

@login_required
@activated_required
@owner_required(model=None)
def post_delete(request, model, object_id, template='posts/post_delete.html', redirect_name=None):
    obj = get_object_or_404(model, id=object_id)
    form = modelform_factory(model, fields=[])(request.POST or None)
    if request.POST and form.is_valid():
        obj.delete()
        messages.add_message(request, messages.SUCCESS, u'Удалено')
        redirect_name = redirect_name if redirect_name else obj.object_name() + '_list'
        return redirect(redirect_name)
    return render(request, template, {
        'object': obj,
        'model': model,
    })

@login_required
@activated_required
@owner_required(model=None)
def post_publish(request, model, object_id):
    obj = get_object_or_404(model, id=object_id)
    form = modelform_factory(model, fields=[])(request.POST or None)
    if request.POST and form.is_valid():
        obj.published = False if obj.published else True
        obj.save()
        messages.add_message(request, messages.SUCCESS, u'Опубликовано' if obj.published else u'Снято с публикации')
    return redirect(request.META.get('HTTP_REFERER'))