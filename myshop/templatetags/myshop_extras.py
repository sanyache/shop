from  django import template

register = template.Library()

@register.filter
def in_category(brands, category):
    return brands.filter(category=category)