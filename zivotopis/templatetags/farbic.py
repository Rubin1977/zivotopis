from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='border_class')
def farbic_class(value):
    try:
        value = int(value)
    except:
        return "text-secondary"
    if value > 0:
        return "text-success"
    elif value < 0:
        return "text-danger"
    else:
        return "text-secondary"

    