# Defines methods used by gamecontroller.py

from game.models import LoggedUser

def login_user(sender, request, user, **kwargs):
	"""
	# Called in gamecontroller.py when user logs in
	# Creates and saves instance of LoggedUser to DB table
	"""
	LoggedUser(username=user.username).save()
	

def logout_user(sender, request, user, **kwargs):
    """
	# Called in gamecontroller.py when user logs out
	# Deletes all instances of LoggedUser from DB table
	"""
	try:
		u = LoggedUser.objects.get(pk=user.username)
		u.delete()
	except LoggedUser.DoesNotExist:
		pass


"""
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import datetime

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
"""