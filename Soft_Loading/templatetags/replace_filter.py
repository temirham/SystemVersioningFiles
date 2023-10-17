from django import template

register = template.Library()

@register.filter(name='replace')
def replace(value, arg):
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)