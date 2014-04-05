from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

from game.gamemetamethods import get_user_who_clicked, add_user_to_waitroom, remove_user_from_waitroom


def lobby(request):
    user = get_user_who_clicked(request)
    remove_user_from_waitroom(user)
    return render(request, 'lobby/lobby.html')


def waitroom(request):
	user = get_user_who_clicked(request)
	add_user_to_waitroom(user)
	return render(request, 'lobby/waitroom.html')