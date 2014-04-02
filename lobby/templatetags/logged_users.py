from django import template
from game.gamemetamethods import get_all_logged_in_users
register = template.Library()

@register.inclusion_tag('lobby/logged_users.html')
def render_logged_in_user_list():
    return { 'users': get_all_logged_in_users() }