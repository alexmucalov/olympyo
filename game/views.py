from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404
from django.db.models import Q, F

from game.models import Action, GameInstanceObject, GameInstance,GameInstanceObjectAttributeValue



def get_action_taken(field):
    # Defines how actions committed to the DB when the number of conceptually-identical
    # fields are committed to the DB, but have to be named differently - e.g., 
    # labour_spots define how many set_wage actions there are, and ActionForm therefore
    # has set_wage_i for all i<=labour_spots - but no arch_action set_wage_i; this is the
    # fix.
    field_split = field.split('_')
    field_last_term = field_split[-1] # Get the last term of the list
    try:
        field_last_term_int = int(field_last_term)
        del field_split[-1]
        action_taken = '_'.join(field_split)
        return action_taken
    except:
        action_taken = field
        return action_taken


def game(request):
    # VARIABLE DEFINITIONS - import from elsewhere?
    user_instance_object = request.user.game_instance_objects.latest()
    alive = True
    game_instance = user_instance_object.game_instance
    instance_id = game_instance.id
    turn = game_instance.turn    
    game_instance_objects = game_instance.game_instance_objects.all()
    display_objects = game_instance_objects.filter(
            game_object__game_object__layout_type__arch_layout='display_object'
    )
    actionform = game_instance.game.game_rules.game_rules
    exec 'from game.forms.%s import ActionForm' % actionform
    
    # DEFINE LIVING AUTONOMOUS OBJECTS, STARVING ONES, AND DEAD ONES
    thriving_auto_objects = GameInstanceObject.objects.filter(
            game_instance__id=instance_id, 
            game_object__game_object__layout_type__arch_layout='autonomous_object', 
            attribute_values__attribute__arch_attribute='wealth', 
            attribute_values__value__gt=2
    )
    starving_auto_objects = GameInstanceObject.objects.filter(
            game_instance__id=instance_id, 
            game_object__game_object__layout_type__arch_layout='autonomous_object', 
            attribute_values__attribute__arch_attribute='wealth', 
            attribute_values__value__gt=0,
            attribute_values__value__lte=2
    )
    dead_auto_objects = GameInstanceObject.objects.filter(
            game_instance__id=instance_id, 
            game_object__game_object__layout_type__arch_layout='autonomous_object', 
            attribute_values__attribute__arch_attribute='wealth', 
            attribute_values__value__lte=0
    )
    living_auto_objects = GameInstanceObject.objects.filter(
            game_instance__id=instance_id, 
            game_object__game_object__layout_type__arch_layout='autonomous_object', 
            attribute_values__attribute__arch_attribute='wealth', 
            attribute_values__value__gt=0
    )
    player_actions = user_instance_object.initiated_actions.all().order_by('-turn')
    player_stats = user_instance_object.attribute_values.all()
    player_arch_game_object = user_instance_object.game_object.game_object.arch_game_object
    player_permitted_initiator_actions = user_instance_object.game_instance.game.action_permission_set.action_permissions.all().filter(
            permitted_initiator__arch_game_object=player_arch_game_object
    )
    player_permitted_action_objects_nondistinct = [
            action.permitted_affected for 
            action in 
            player_permitted_initiator_actions
    ]
    player_permitted_action_objects = list(
            set(player_permitted_action_objects_nondistinct)
    )
    
    
    # CONDITIONS: If game over, game/over/; if player dead, dead
    if float(turn) > float(game_instance.game.turns):
        return HttpResponseRedirect('/game/over/')
    
    user_wealth_attr = user_instance_object.attribute_values.all().get(
            attribute__arch_attribute='wealth'
    )
    if float(user_wealth_attr.value) <= 0:
        alive = False


    # SELECTED OBJECT DEFINITION
    game_object = None
    game_object_owner_set = None
    if 'game_object_id' in request.GET:
        game_object_id = request.GET['game_object_id']
        game_object = GameInstanceObject.objects.get(id=game_object_id)
        try:
            game_object_owner_set = game_instance_objects.filter(
                    relationship_subjects__relationship__arch_relationship='owns',
                    relationship_subjects__object_game_instance_object__id=game_object_id
            )   
        except:
            pass
    
    
    # CORE VIEW LOGIC
    if request.method=='POST':
        action_form = ActionForm(request.POST)
        if action_form.is_valid():
            user_already_played = True
            cleaned_data = action_form.cleaned_data
            
            # Post actions to the DB
            for field in cleaned_data:
                if cleaned_data[field] is not None:
                    action_taken = get_action_taken(field)
                    parameters = cleaned_data[field]
                    user_instance_object.act(action_taken, parameters, game_object_id)
            
            # Check DB to see if all living users have committed actions; update turn if so
            living_players = living_auto_objects.filter(game_object__game_object__arch_game_object='player')
            i = 0
            for gio in living_players:
                if not gio.initiated_actions.all().filter(turn=turn).exists(): break
                else: i += 1
            if i != len(living_players): pass
            else:
                game_instance.update_turn()
                return HttpResponseRedirect('/game/')


        else:
            user_already_played = False

    else:
        user_already_played = False
        action_form = ActionForm(initial={'work': 'no'})  
        user_turn_action_set = Action.objects.filter(
                turn=turn, 
                initiator=user_instance_object
        )
        if user_turn_action_set:
            user_already_played = True


    return render(request, 'game/game.html', {
            'user_instance_object': user_instance_object, 
            'alive': alive,
            'display_objects': display_objects, 
            'player_stats': player_stats, 
            'thriving_auto_objects': thriving_auto_objects, 
            'starving_auto_objects': starving_auto_objects, 
            'dead_auto_objects': dead_auto_objects, 
            'game_object': game_object, 
            'player_permitted_action_objects': player_permitted_action_objects, 
            'game_object_owner_set': game_object_owner_set, 
            'action_form': action_form, 
            'turn': turn, 
            'user_already_played': user_already_played
    })
    #For now, permit centre_display with at most two elements 
    #Later, include timer: http://keith-wood.name/countdown.html



def game_over(request):
    user_instance_object = request.user.game_instance_objects.latest()
    game_instance = user_instance_object.game_instance
    ordered_players_leisure_attrs = GameInstanceObjectAttributeValue.objects.filter(
            game_instance_object__game_instance=game_instance, 
            game_instance_object__game_object__game_object__arch_game_object='player', 
            attribute__arch_attribute='leisure'
    ).order_by('-value')
    ordered_players = [attr.game_instance_object for attr in ordered_players_leisure_attrs]
    # Placement works, but this isn't the greatest: uses == instead of is:
    # is doesn't work, I suspect because I created new objects with the ordered_players
    # list comprehension - should find a better way
    
    placement = ''

    if user_instance_object == ordered_players[0]:
        placement = 'first_place'
    elif user_instance_object == ordered_players[-1]:
        placement = 'last_place'
    #elif user_instance_object is in ordered_players[:2]:
        #placement = 'top_three'


    return render(request, 'game/game_over.html', {'placement': placement})