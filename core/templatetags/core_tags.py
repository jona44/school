from django import template
from core.utils import get_school_logo

register = template.Library()

@register.simple_tag
def get_school_logo_template(user):
    return get_school_logo(user)