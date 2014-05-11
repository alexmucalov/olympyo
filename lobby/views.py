from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404

from game.models import GameInstanceObject, Game, Waitroom

def lobby(request):    
    waitrooms = request.user.waitrooms.all()
    try:
        for waitroom in waitrooms:
            waitroom.remove_user(request.user)
    except:
        pass

    games = Game.objects.all()
    game = None
    game_player_count = None
    if 'game_id' in request.GET:
        game_id = request.GET['game_id']
        game = Game.objects.get(id=game_id)
        game_player_count = game.game_object_set.game_objects.all().filter(
                game_object__arch_game_object='player'
                ).count()
    
    if 'create_waitroom' in request.GET:
        new_waitroom = Waitroom.objects.create_waitroom(game=game, users=request.user)
        return HttpResponseRedirect('/waitroom/?waitroom_id=' + str(new_waitroom.id))
    
    waitroom = None
    if 'waitroom_id' in request.GET:
        waitroom_id = request.GET['waitroom_id']
        waitroom = Waitroom.objects.get(id=waitroom_id)

    return render(request, 'lobby/lobby.html', {
            'games': games,
            'game': game,
            'game_player_count': game_player_count,
            'waitroom': waitroom,
            })

def waitroom(request):
	waitroom_id = request.GET['waitroom_id']
	try:
	    waitroom = Waitroom.objects.get(id=waitroom_id)
	except:
	    return HttpResponseRedirect('/game/')
	waitroom.add_user(request.user)
	try:
	    waitroom = Waitroom.objects.get(id=waitroom_id)
	except:
	    return HttpResponseRedirect('/game/')
	    
	return render(request, 'lobby/waitroom.html')