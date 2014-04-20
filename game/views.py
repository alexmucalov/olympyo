from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

from game.models import Action

def game(request):
    user = request.user
    
    #Assuming for now that each player only "is" one game object... okay! Because can
    #control 'owned' objects through relationship table
    game_instance_object = user.game_instance_objects.latest()
    game_instance = game_instance_object.game_instance
    
    
    #timer =
    #Later, include timer: http://keith-wood.name/countdown.html 
    
    #What actions has a player committed? What were the results?
    player_action_log = Action.objects.filter(initiator=game_instance_object).order_by("-turn")
    
    #What do the player's current wealth and leisure look like?
    player_stats = game_instance_object.attribute_values.all()
    
    #What objects can a player commit actions on? Tough... Leave out for now
    #action_objects = 
    
    #What are displayed objects' attribute_values and relationships to other objects?
    #object_stats_and_rels = Use ajax instead, here!
    
    #For a given action_object, what are the available actions? E.g., for a farm that a
    #player owns, can set_wage or work
    #available_actions = Use ajax instead, here!
    
    
    
    return render(request, 'game/game.html')