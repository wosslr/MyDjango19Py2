from django import template

register = template.Library()


@register.filter(name='set_class')
def set_class(value, arg):
    # return value.as_widget(attrs={'class': arg})
    value.field.widget.attrs['class'] = arg
    return value


@register.filter(name='set_pholder')
def set_pholder(value, arg):
    # return value.as_widget(attrs={'class': arg})
    value.field.widget.attrs['placeholder'] = arg
    return value

@register.filter(name='set_default')
def set_value(value, arg):
    value.field.widget.attrs['default_value'] = arg
    return value
