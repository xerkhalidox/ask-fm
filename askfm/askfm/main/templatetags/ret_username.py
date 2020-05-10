from django import template
from django.contrib.auth import get_user_model
from django.template.defaultfilters import stringfilter

register=template.Library()

@register.filter
@stringfilter
def ret_username(id):
    username=get_user_model().objects.get(id=id).username
    return username