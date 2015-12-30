from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from django.forms.models import inlineformset_factory, modelformset_factory, formset_factory, modelform_factory

from apps.tests.models import Test, TestCase

def test(request):

    test_id = request.session.get('test', None)

    if test_id:

        test = get_object_or_404(Test, id=test_id)
        test_form    = modelform_factory(Test, fields=['title'])(data=request.POST or None, files=request.FILES or None, instance=test)
        test_formset = inlineformset_factory(Test, TestCase, can_delete=True, extra=0, **TestCase.form_params)(data=request.POST or None, files=request.FILES or None, instance=test) # А если не can_delete то чё?

        if request.POST and test_form.is_valid() and test_formset.is_valid():

            new_event      = test_form.save(commit=False)
            new_event.save()

            test_form.save_m2m()

            test_formset.instance = new_event
            test_formset.save()

            messages.add_message(request, messages.SUCCESS, u'Сохранено')

            return redirect(request.POST['next'])

    return redirect(request.META.get('HTTP_REFERER'))

def start_test(request, test_id):
    request.session['test'] = test_id
    return redirect(request.META.get('HTTP_REFERER'))

def end_test(request):
    del request.session['test']
    return redirect(request.META.get('HTTP_REFERER'))