# Defines methods used by gamecontroller.py

from game.models import ActiveUser, Game
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import datetime


def get_user_who_clicked(request):
	user = request.user
	return user


def add_user_to_waitroom(u):
	# For now, only one game
	g = Game.objects.get(id=4)
	ActiveUser(user=u, game=g, launched=False).save()
	

def remove_user_from_waitroom(u):
    try:
		uid = ActiveUser.objects.get(user=u)
		uid.delete()
    except ActiveUser.DoesNotExist:
		pass


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


def get_all_waitroom_users():
	waitroom_users = ActiveUser.objects.all()
	return waitroom_users
