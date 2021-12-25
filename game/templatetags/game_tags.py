from django import template

register = template.Library()


@register.filter
def not_soft_deleted_count(games):
    return games.filter(is_deleted=False).count()
