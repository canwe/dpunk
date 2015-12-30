from django.conf import settings

from apps.tests.utils import get_test_forms

def site(request):

    test_form, test_formset = get_test_forms(request)

    return {
        'url_name': request.resolver_match.url_name,
        'settings': settings,
        'test_form': test_form,
        'test_formset': test_formset,
    }