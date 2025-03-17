from django import template
from django.urls import reverse

register = template.Library()
@register.simple_tag
def get_dashboard_url(user):
    if user.groups.filter(name='student').exists():
        return reverse('student_dashboard')
    elif user.groups.filter(name='staff').exists():
        return reverse('teacher_dashboard')
    elif user.groups.filter(name='school_admin').exists():
        return reverse('school_admin_dashboard')
    elif user.groups.filter(name='deputy_head').exists():
        return reverse('deputy_head_dashboard')
    elif user.groups.filter(name='school_head').exists():
        return reverse('school_head_dashboard')
    else:
        return reverse('default_dashboard')
    
    
   
@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})    



@register.filter
def get_item(queryset, key):
    """
    Gets the first item from a queryset where the id matches the key.
    """
    try:
        return queryset.get(id=key)  # Use filter and take the first element
    except Exception as e:
        # Handle the case where no such item exists or MultipleObjectsReturned
        return None

