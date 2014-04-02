from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404



def login_user(sender, request, user, **kwargs):
	"""
	# Called in gamecontroller.py when user logs in
	# Creates and saves instance of LoggedUser to DB table
	"""
	LoggedUser(username=user.username).save()

def lobby(request):
    return render(request, 'lobby/lobby.html')




# When waitroom called by a user's click on a link in the lobby, waitroom function 
# should be passed the user object who clicked the link
# So, query session_id of user who clicks, and return user object...


"""
* Lobby will show all non-expired users (by session) - see link in gamemetamethods
* Waitroom will show all users who entered waitroom
* Game launch will enter all those users from waitroom
"""

def waitroom(request):
    #
    return render(request, 'lobby/waitroom.html')