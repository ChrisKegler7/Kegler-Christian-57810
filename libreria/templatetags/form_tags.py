from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    if hasattr(field, 'field'):
        field.field.widget.attrs['class'] = css_class
    return field

