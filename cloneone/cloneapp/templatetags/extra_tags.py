from django import template
from cloneapp.models import user_info
from django.shortcuts import get_object_or_404

register = template.Library()

@register.filter(name='imageurl')
def image_url(value):
    k=get_object_or_404(user_info,user_p = value)
    return k.image_field.url
