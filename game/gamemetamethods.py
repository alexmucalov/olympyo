# Defines methods used by gamecontroller.py

from game.models import Game
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import datetime



"""
Waitroom
"""

"""
Define these as instance methods, instead


def add_user_to_waitroom(game, user):
	# For now, only one game
	#game = Game.objects.get(id=4)
	GameUser.objects.create(user=user, game=game, launched=False)
	#assign_user_to_player(user)
	

def remove_user_from_waitroom(u):
    try:
		uid = ActiveUser.objects.get(user=u)
		uid.delete()
    except ActiveUser.DoesNotExist:
		pass
# Use Boolean flag instead of adding or deleting from rows - in process


def get_all_waitroom_users():
	waitroom_users = ActiveUser.objects.all()
	return waitroom_users


def assign_user_to_player(u):
	pass
"""


"""
Lobby
"""
def get_all_logged_in_users():
    # Query all non-expired sessions
    sessions = Session.objects.filter(expire_date__gte=datetime.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)


