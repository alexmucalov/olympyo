# Defines methods used by gamecontroller.py

from game.models import LoggedUser
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import datetime


def get_user_who_clicked(request):
	user = request.user
	return user


def add_user_to_waitroom(user):
	LoggedUser(username=user.username).save()
	

def remove_user_from_waitroom(user):
    try:
		u = LoggedUser.objects.get(pk=user.username)
		u.delete()
    except LoggedUser.DoesNotExist:
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
	waitroom_users = LoggedUser.objects.all()
	return waitroom_users