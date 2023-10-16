from django import template

register = template.Library()

@register.filter(name='add_space_separator')
def add_space_separator(value):
    return '{:,}'.format(value).replace(',', ' ')


@register.simple_tag(takes_context=True)
def remove_tag(context, tag_to_remove):
    query_string = context['request'].GET.copy()
    if tag_to_remove in query_string:
        del query_string[tag_to_remove]

    return query_string.urlencode()