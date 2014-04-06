from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

#from game.gamemetamethods import get_user_who_clicked, add_user_to_waitroom, remove_user_from_waitroom


def lobby(request):
    #user = request.user
    #remove_user_from_waitroom(user)
    return render(request, 'lobby/lobby.html')


def waitroom(request):
	#user = request.user
	#add_user_to_waitroom(user)
	return render(request, 'lobby/waitroom.html')


"""
def register_user_for_game(request):
	game = Game.objects.get(id=request.GET.get('game_id'))
	users = ...
	game_user = game.game_users.create(user=request.user, game, instance=None)
	if GameUser.objects.filter(game=game, instance=None).count() >= game.minimum_players:
		game.create_instance(users)
"""

"""
def lobby(request):
	game = Game.objects.get(id=request.GET.get('game_id'))
	user = request.user
	game.add_user_to_waitroom(user)
"""