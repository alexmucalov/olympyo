from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

def game(request):
    return render(request, 'game/game.html')