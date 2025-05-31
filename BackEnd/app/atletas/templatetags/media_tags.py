from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def media_url(path):
    return f"{settings.MEDIA_URL}{path}"