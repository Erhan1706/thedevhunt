from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup
from datetime import datetime, timezone

register = template.Library()

@register.filter
@stringfilter
def escape_slug(value):
  return value.replace(".","_")

@register.filter
@stringfilter
def escape_css_class(value):
    return value.replace(".", "-")

@register.filter(name='clean_html')
def clean_html(value):
    """
    Clean the HTML content, by closing any unclosed tags.
    """
    soup = BeautifulSoup(value, 'html.parser')
    return mark_safe(str(soup))

@register.filter
def days_since_posted(date):
    """
    Returns the number of days since the date passed in.
    """
    if not date:
        return ''
    b = datetime.now()
    delta = datetime.now(timezone.utc) - date
    if delta.days > 0:
        return f'{delta.days}d ago'
    else:
        hours = delta.seconds // 3600 
        return f'{hours}h ago'
    
@register.filter
def multiply(value, arg):
    return int(value) * int(arg)