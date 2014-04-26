from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404

from game.models import Action, GameInstanceObject
from game.forms.farm_village import OwnedFarmActionForm


def get_action_taken(field):
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
    user = request.user
    user_instance_object = user.game_instance_objects.latest()
    game_instance = user_instance_object.game_instance
    game_instance_objects = game_instance.game_instance_objects.all()
    display_objects = game_instance_objects.filter(game_object__game_object__layout_type__arch_layout='display_object')
    autonomous_objects = game_instance_objects.filter(game_object__game_object__layout_type__arch_layout='autonomous_object')
    player_actions = user_instance_object.initiated_actions.all().order_by('-turn')
    player_stats = user_instance_object.attribute_values.all()
    player_arch_game_object = user_instance_object.game_object.game_object.arch_game_object
    player_permitted_initiator_actions = user_instance_object.game_instance.game.action_permission_set.action_permissions.all().filter(permitted_initiator__arch_game_object=player_arch_game_object)
    player_permitted_action_objects_nondistinct = [action.permitted_affected for action in player_permitted_initiator_actions]
    player_permitted_action_objects = list(set(player_permitted_action_objects_nondistinct))
    
    display_rules = game_instance.game.display_ruleset.arch_display_ruleset
    exec 'from game.display_rules.%s import centre_displays' % display_rules
    centre_display = centre_displays(game_instance)
    
    # Dynamically import the right game_forms, instead of the way done at top; = ...

    game_object = None
    game_object_owner_set = None
    if 'game_object_id' in request.GET:
        game_object_id = request.GET['game_object_id']
        game_object = GameInstanceObject.objects.get(id=game_object_id)
        try:
            game_object_ownership_relationships = game_object.relationship_objects.all().filter(relationship__arch_relationship='owns')
            game_object_owner_set = [relationship.subject_game_instance_object for relationship in game_object_ownership_relationships]
            #if user has already committed an action this turn, pass True to Boolean variable in context
            #And use template to grey out the action_form
        except:
            pass
    
    if request.method=='POST':
        action_form = OwnedFarmActionForm(request.POST)
        if action_form.is_valid():
            cd = action_form.cleaned_data
            for field in cd:
                action_taken = get_action_taken(field)
                parameters = cd[field]
                user_instance_object.act(action_taken, parameters, game_object_id)
        else:
            pass
            #Populate action_form.errors
            #Pass this into the context? How do errors work?
    else:
        action_form = OwnedFarmActionForm()    
    
    return render(request, 'game/game.html', {'user_instance_object': user_instance_object, 'centre_display': centre_display, 'display_objects': display_objects, 'player_stats': player_stats, 'autonomous_objects': autonomous_objects, 'game_object': game_object, 'player_permitted_action_objects': player_permitted_action_objects, 'game_object_owner_set': game_object_owner_set, 'action_form': action_form})
    #For now, permit centre_display with at most two elements 
    #Later, include timer: http://keith-wood.name/countdown.html 