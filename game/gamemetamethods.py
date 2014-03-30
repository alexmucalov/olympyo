# Defines methods used by gamecontroller.py

from game.models import LoggedUser


def login_user(sender, request, user, **kwargs):
  	"""
	Called in gamecontroller.py when user logs in
	Creates and saves instance of LoggedUser to DB table
	"""
	LoggedUser(username=user.username).save()


def logout_user(sender, request, user, **kwargs):
    """
	Called in gamecontroller.py when user logs out
	Deletes all instances of LoggedUser from DB table
	"""
	try:
		u = LoggedUser.objects.get(pk=user.username)
		u.delete()
	except LoggedUser.DoesNotExist:
		pass