from django import template

register = template.Library()


@register.filter
def not_soft_deleted_count(games):
    """Tag for counting number of users added a particular game to their musts"""

    return games.filter(is_deleted=False).count()
