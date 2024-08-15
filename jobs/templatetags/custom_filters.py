from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def escape_slug(value):
  return value.replace(".","_")