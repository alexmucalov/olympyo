from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

#from game.metamethods import get_user_who_clicked, add_user_to_waitroom, remove_user_from_waitroom
from game.models import GameInstanceObject

def lobby(request):
    #user = request.user
    #remove_user_from_waitroom(user)
    return render(request, 'lobby/lobby.html')


def waitroom(request):
	#user = request.user
	#add_user_to_waitroom(user)
	
	#if a gio exists for user, then render option for user to enter game
	try:
	    user_instance_object = request.user.game_instance_objects.latest()
	    game_exists = True
	except:
	    game_exists = False

	    
	return render(request, 'lobby/waitroom.html', {'game_exists': game_exists})