from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

from game.models import Action, GameInstanceObject

def game(request):
    user = request.user
    user_instance_object = user.game_instance_objects.latest()
    game_instance = user_instance_object.game_instance
    game_instance_objects = game_instance.game_instance_objects.all()
    display_objects = game_instance_objects.filter(game_object__game_object__layout_type__arch_layout='display_object')
    autonomous_objects = game_instance_objects.filter(game_object__game_object__layout_type__arch_layout='autonomous_object')
    player_actions = user_instance_object.initiated_actions.all().order_by('-turn')
    player_stats = user_instance_object.attribute_values.all()
    
    display_rules = game_instance.game.display_ruleset.arch_display_ruleset
    exec 'from game.display_rules.%s import centre_displays' % display_rules
    centre_display = centre_displays(game_instance)

    game_object = None
    if 'game_object_id' in request.GET:
        game_object_id = request.GET['game_object_id']
        game_object = GameInstanceObject.objects.get(id=game_object_id)
    
    return render(request, 'game/game.html', {'centre_display': centre_display, 'display_objects': display_objects, 'player_stats': player_stats, 'autonomous_objects': autonomous_objects, 'game_object': game_object})
    #For now, permit centre_display with at most two elements 
    #Later, include timer: http://keith-wood.name/countdown.html 