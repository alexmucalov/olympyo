from django import template
from game.gamemetamethods import get_all_logged_in_users, get_all_waitroom_users
register = template.Library()


@register.inclusion_tag('lobby/logged_users.html')
def render_logged_in_user_list():
    return { 'logged_users': get_all_logged_in_users() }


@register.inclusion_tag('lobby/waitroom_users.html')
def render_waitroom_user_list():
    return { 'waitroom_users': get_all_waitroom_users() }