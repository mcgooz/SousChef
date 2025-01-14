from django import template

register = template.Library()

@register.filter
def custom_floatformat(value):
    return ('%.2f' % value).rstrip('0').rstrip('.')

@register.filter
def zip_lists(a, b):
    return zip(a, b)