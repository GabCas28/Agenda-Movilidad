from django import template
register = template.Library()

@register.inclusion_tag('side_menu.html', takes_context=True)
def side_menu(context):
    return {
        'menu_items': context['menu_items'] if 'menu_items' in context else None,
        'menu_title': context['menu_title'] if 'menu_title' in context else None,
        'menu_type': context['menu_type'] if 'menu_type' in context else None
        }   