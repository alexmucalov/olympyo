"""
specifies turn update logic for version 1 rules
		-2div-v, below
		-imports from gameforms.py for specific actions' forms (useful for validating)
		-defines the game functions that each view function will call when a given button 
			is pressed
		-(When you POST, you post to the same urlconf, which calls a view function, which 
			can in turn call any other function you want - but you want to keep views and
			game logic separate! Want refreshed pages to query all players' updated info?
			Or keep all hidden? Or keep all other players' info hidden? Not difficult, no
			matter what.)
			-- Push public/private wage display, e.g., back to game rules, and leave as 
				an argument in game rules' functions
			-- Leave as arguments, for game rules to read, things like player_wage_info
				(public or private), farm_productivity_parameter (squared, cubed, etc.)
			-- Put these parameters in the DB attached to each game, under something like
				a rule_parameters column and a rule_values column, and have the game 
				rules query those parameters and store those values locally when a 
				game_init function is called
		-So:
			-- On a turn, gamerules house the DB query functions that views will call
			-- When turns update - called by gamecontroller - gamerules will update state,
				per 2dv. below; and then gamecontroller (?) will log all changes
"""
"""
And when the turn timer runs out, the game engine has to operate over the
			actions committed that turn, and correctly calculate the next game state
			- At first, just let owners choose whether to work one of their own plots,
				assign labour to wages, and calculate new state: 
				-- Query AI labour count at a given turn
				-- Sort player wages entered in a given turn
				-- Find top (labour_count) wages, and assign AI labourers to positions
					(randomly? Does each AI labourer have an identity? Yes - more robust)
				-- Then, for each farm, calculate production:
					--- If farm_labour_count == 2: farm_production = 4
					--- If farm_labour_count == 1: farm_production = 1
					--- If farm_labour_count == 0: farm_production = 0
				-- Update food_counts:
					--- If owner_food_count + farm_production > sum of wages
						Then each AI gets wage, player gets farm_production - wages
					--- Else: AI gets owner_food_count + farm_production,
						owner dies
				-- Update player_leisure_count:
					--- If owner didn't work: player_leisure_count += 1
					--- If AI didn't work: AI_leisure_count += 1
					--- ** What conditions dictate that AI won't work in a turn??
						Use something as close to the most basic micro model, to test!
"""
from django.db.models import Q
from django.db.models import F

#Nomic; make it possible to encapsulate a rule, as a part of a ruleset, and store it somewhere (in a databaset) so that users can share them!

#def update_turn(instance_id, turn):
    #First, have labour take action to take wages:
    
    #set_wage_actions = Action.objects.filter(initiator.game_instance.id__exact=instance_id, turn__exact=turn, action.arch_action__exact='set_wage')
    #sorted_set_wage_actions = set_wage_actions.order_by('parameters')
    #labour = GameInstanceObject.objects.get(game_instance.id__exact=instance_id, game_object.game_object.arch_game_object__exact='labour')
    #labour_and_wages_offered = zip(labour, sorted_set_wage actions)
    #for (labourer, wage_offered) in labour and wages_offered:
        #labourer.act('work')
        #labourer.act('take_wage', wage_offered.parameters, wage_offered.affected)

    
    #Second, reset labour_working on each farm:
    
    #farms = GameInstanceObject.objects.filter(game_instance.id__exact=instance_id, game_object.game_object.arch_game_object__exact='farm')
    #for farm in farms:
        #labour_working_attr = farm.attribute_values.get(attribute='labour_working')
        #labour_working_attr.value = 0
        #labour_working_attr.save(update_fields=['value'])


    #Third, determine which players worked their own farms, and increment labour_working if they are:
    
    #players_who_worked_farms = GameInstanceObject.objects.filter(game_instance.id__exact=instance_id, game_object.game_object.arch_game_object__exact='player', initiated_actions.turn__exact=turn, initiated_actions.action__exact='work')
    #for player in players_who_worked_farms:
        #player_farm = player.relationship_subjects.get(relationship.arch_relationship='owns').object_game_instance_object
        #labour_working_attr = player_farm.attribute_values.get(attribute='labour_working')
        #labour_working_attr.value = F('value') + 1
        #labour_working_attr.save(update_fields=['value'])
    
    
    #Fourth, recalculate total labour_working on each farm:

    #worked_farms = GameInstanceObject.objects.filter(game_instance.id__exact=instance_id, game_instance.turn__exact=turn, affected_by_actions.action.arch_action__exact='set_wage', affected_by_actions.action.arch_action__exact='take_wage')
    #for farm in worked_farms:
        #count_set_wage_actions = farm.affected_by_actions.filter(action.arch_action__exact='set_wage').count()
        #count_take_wage_actions = farm.affected_by_actions.filter(action.arch_action__exact='take_wage').count()
        #labour_working = min(count_set_wage_actions, count_take_wage_actions)
        #labour_working_attr = farm.attribute_values.get(attribute__exact='labour_working')
        #labour_working_attr.value = F('value') + labour_working
        #labour_working_attr.save(update_fields=['value'])


    #Fifth, calculate this turn's production:
    
    #for each farm in farms:
        #production_attr = farm.attribute_values.get(attribute__exact='production')
        #labour_working_attr = farm.attribute_values.get(attribute__exact='labour_working')
        #productivity_attr = farm.attribute_values.get(attribute__exact='productivity')
        #production_attr.value = labour_working_attr.value ** productivity_attr.value
        #production_attr.save(update_fields=['value'])


    #Sixth, update all players' and labourers' wealth and leisure:
    
    #LEISURE
    #labourers_who_didnt_work = GameInstanceObject.objects.filter(game_instance.id__exact=instance_id, game_object.game_object.arch_game_object__exact='labour', initiated_actions.turn__exact=turn, ~Q(initiated_actions.action__exact='work'))
    #players_who_didnt_work = GameInstanceObject.objects.filter(game_instance.id__exact=instance_id, game_object.game_object.arch_game_object__exact='player', initiated_actions.turn__exact=turn, ~Q(initiated_actions.action__exact='work'))
    #for labour in labourers_who_didnt_work:
        #leisure_attr = labour.attribute_values.get(attribute__exact='leisure')
        #leisure_attr.value = F('value') + 1
        #leisure_attr.save(update_fields = ['value'])
    #for player in players_who_didnt_work:
        #leisure_attr = player.attribute_values.get(attribute__exact='leisure')
        #leisure_attr.value = F('value') + 1
        #leisure_attr.save(update_fields = ['value'])
    #WEALTH
    #

    # !!! Get a queryset of all players filtered to turn=1 and game instance=1 !!!