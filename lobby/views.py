from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

def lobby(request):
    return render(request, 'lobby/lobby.html')
    
def waitroom(request):
    return render(request, 'lobby/waitroom.html')