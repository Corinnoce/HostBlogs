from django import template
import re

register = template.Library()

@register.filter
def strong(value):
    return re.sub(r'\*(.*?)\*', r'<h4>\1</h4>', value)

@register.filter
def list(value):
    return re.sub(r'\#(.*?)\#', r'<li>\1</li>', value)