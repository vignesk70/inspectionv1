from __future__ import unicode_literals
from django.utils.safestring import mark_safe

from django import template
import json

register = template.Library()


@register.filter('has_group')
def has_group(user, group_name):
    """
    Verifica se este usuário pertence a um grupo
    """
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False


@register.filter('js')
def js(obj):
    return mark_safe(json.dumps(obj))
