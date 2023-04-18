from django import template
register = template.Library()

@register.inclusion_tag('navigation.html', takes_context=True)
def navigation(context):
    return {
        'request': context.request
    }   