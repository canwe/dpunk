# -*- coding: utf-8 -*-

from django import template
from django.utils import timezone
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, url_name, *url_params):
    if url_params and reverse(url_name, args=url_params) == context['request'].path:
        return ' active'
    if not url_params and reverse(url_name) == context['request'].path:
        return ' active'
    return ''

@register.simple_tag(takes_context=True)
def active_child(context, url_names):
    url_names = url_names.split(',')
    for url_name in url_names:
        if reverse(url_name.strip()) == context['request'].path:
            return ' active-child'
    return ''

@register.filter
def form(value):

    value.required_css_class, value.error_css_class = 'required', 'error'

    value = value._html_output(
        normal_row             = '<span class="form-field form-field-%(field_name)s remove_class%(html_class_attr)sremove_class"><span class="form-label">%(label)s <span class="form-errors">%(errors)s</span>%(help_text)s</span><span class="form-input">%(field)s</span></span>',
        error_row              = '<span><span></span><span>%s</span></span>',
        row_ender              = '</span></span>',
        help_text_html         = '<span class="helptext">%s</span>',
        errors_on_separate_row = False,
    )

    value = value.replace('remove_class class="', '').replace('"remove_class', '').replace('remove_class', '')
    value = value.replace(':</label>', '</label>').replace('.</li>', '</li>')
    return value