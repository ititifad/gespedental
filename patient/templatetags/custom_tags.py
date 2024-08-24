# yourapp/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.filter
def split_string(value):
    """Splits a string into a list."""
    return value.split()
