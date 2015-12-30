from django.shortcuts import get_object_or_404
from django.forms.models import inlineformset_factory, modelform_factory

from apps.tests.models import Test, TestCase

def get_test_forms(request):

    test_form, test_formset = None, None

    test_id = request.session.get('test', None)

    if test_id:
        test         = get_object_or_404(Test, id=test_id)
        test_form    = modelform_factory(Test, fields=['title'])(data=request.POST or None, files=request.FILES or None, instance=test)
        test_formset = inlineformset_factory(Test, TestCase, can_delete=True, extra=0, **TestCase.form_params)(data=request.POST or None, files=request.FILES or None, instance=test) # А если не can_delete то чё?

    return test_form, test_formset