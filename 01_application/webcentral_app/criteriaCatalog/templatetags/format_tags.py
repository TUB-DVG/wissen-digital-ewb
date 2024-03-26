from django import template

register = template.Library()

@register.filter
def format_tags(tags):
    # breakpoint()
    return ', '.join(str(tag) for tag in tags.all())
