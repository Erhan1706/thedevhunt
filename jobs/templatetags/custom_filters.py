from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup

register = template.Library()

@register.filter
@stringfilter
def escape_slug(value):
  return value.replace(".","_")

@register.filter(name='clean_html')
def clean_html(value):
    """
    Clean the HTML content, by closing any unclosed tags.
    """
    soup = BeautifulSoup(value, 'html.parser')
    return mark_safe(str(soup))