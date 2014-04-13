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
from django.db.models import Q, F
from game.game_rules.components import eat, reset_labour_working, work_own_farm, labour_worked, produce, earn, profit, enjoy_leisure
from game.models import *
"""
*** Intended initial DB definition ***

*Arch_actions: work, take_wage, set_wage
*Arch_attribute_sets: normal_player, normal_labour, normal_farm
*Arch_attributes: productivity, labour_spots, labour_working, production, cost, leisure, wealth
*Arch_game_objects: player, labour, farm, nature
*Arch_game_object_attribute_values: [farm, labour_working, 0], [farm, labour_spots, 2], [farm, production, 0], [farm, productivity, 2], [farm, cost, 2], [player, leisure, 0], [player, wealth, 2], [labour, leisure, 0], [labour, wealth, 2]
*Attribute_values: as directly above, but with 'normal_' prepended to each game_object
*Game_object_relationship_sets: modest_ownership
*Game_objects: [farm_village, player, normal_player]*2, [farm_village, labour, normal_labour]*3, [farm_village, farm, normal_farm]*2, [farm_village, nature, (None)]
*Game_object_relationships:[modest_ownership, player1, owns, farm1], [modest_ownership, player2, owns, farm2]
*Games: [farm_village_modest_ownership, farm_village, modest_ownership, v1, 20]
*Game_instances: [farm_village_modest_ownership, 1]
*Game_instance_objects: as in Game_objects, but attach players to users
*Game_instance_object_relationships: as in Game_object_relationships, for a given game instance
*Game_instance_object_attribute_values: according to Attribute_values, but for each game_instance_object (20 records total)
*Actions: GIO players 1 and 2 can set two wages each - each affecting their own farms - to test

*Note: All game_instance tables should be populated properly as part of 'Game' instance method 'create_game_instance', referenced below
*Add 'alive' as a Bool attr for players and labourers? Yes - but later; then condition any player or labour activity on players or labourers being alive
"""
"""
NOTES
#Nomic; make it possible to encapsulate a rule, as a part of a ruleset, and store it somewhere (in a databaset) so that users can share them!
#Put under instance method 'create_game_instance': create all game instance objects, and create all their starting attributes... BE CAREFUL WITH THIS - COULD BE INVOLVED
#Use map, here
"""

# Instance method on GameInstance objects; ruleset is called dynamically 
def update_turn(instance):
    instance_id = instance.id
    turn = instance.turn
    
    #Players and labourers eat 1 wealth:
    players = GameInstanceObject.objects.filter(game_instance.id__exact=instance_id, game_object.game_object.arch_game_object__exact='player')
    labourers = GameInstanceObject.objects.filter(game_instance.id__exact=instance_id, game_object.game_object.arch_game_object__exact='labour')
    for player in players:
        player.eat()
    for labour in labourers:
        labour.eat()

    #Farms reset labour_working to zero:
    farms = GameInstanceObject.objects.filter(game_instance.id__exact=instance_id, game_object.game_object.arch_game_object__exact='farm')
    for farm in farms:
        farm.reset_labour_working()
    
    #Farm increases labour_working by one if its owner worked it
    players_who_worked_farms = GameInstanceObject.objects.filter(game_instance.id__exact=instance_id, game_object.game_object.arch_game_object__exact='player', initiated_actions.turn__exact=turn, initiated_actions.action__exact='work')
    for player in players_who_worked_farms:
        player.work_own_farm()
    
    #Have labour take action to take wages, work, and get paid:
    sorted_set_wage_actions = Action.objects.filter(initiator.game_instance.id__exact=instance_id, turn__exact=turn, action.arch_action__exact='set_wage').order_by('-parameters')
    labour_and_wages_offered = zip(labourers, sorted_set_wage actions)
    for (labour, wage_offered) in labour_and_wages_offered:
        labour.act('take_wage', wage_offered.parameters, wage_offered.affected)
        labour.act('work')
    
    #Farm increases labour_working for all labourers working it:
    worked_farms = GameInstanceObject.objects.filter(game_instance.id__exact=instance_id, game_instance.turn__exact=turn, affected_by_actions.action.arch_action__exact='set_wage', affected_by_actions.action.arch_action__exact='take_wage')
    for farm in worked_farms:
        farm.labour_worked()

    #Farms produce based on total labour_working, then split production between wages and profits:
    for farm in farms:
        farm.produce()
        
        # Common source values
        farm_production_attr = farm.attribute_values.get(attribute__exact='production')
        farm_owner = farm.relationship_objects.get(relationship__exact='owns').subject_game_instance_object
        farm_owner_wealth_attr = owner.attribute_values.get(attribute__exact='wealth')
        farm_labour_actions = farm.affected_by_actions.filter(action__exact='take_wage', turn__exact=turn)
        labour_count = len(farm_labour_actions)
        farm_wages_offered = []
        for farm_labour_action in farm_labour_actions:
            farm_wage_offered = [farm_labour_action.parameters]
            farm_wages_offered = farm_wages_offered + farm_wage_offered
        
        # If owner can pay all costs, do so, then keep the rest
        if farm_owner_wealth_attr.value + farm_production_attr.value >= sum(farm_wages_offered):
            farm_labour_costs = 0
            for farm_labour_action in farm_labour_actions:
                farm_wage_offered = farm_labour_action.parameters
                farm_labour_costs += farm_wage_offered
                farm_labour_wealth_attr = farm_labour_action.initiator.attribute_values.get(attribute__exact='wealth')
                farm_labour_wealth_attr.value = F('value') + farm_wage_offered
                farm_labour_wealth_attr.save(update_fields['value'])
            farm_owner_wealth_attr.value = F('value') + farm_production_attr - farm_labour_costs
            farm_owner_wealth_attr.save(update_fields=['value'])
        
        # If owner can't pay all the costs, pay as much as possible evenly among all labourers, then set owner wealth = 0
        else:
            farm_labour_costs = farm_owner_wealth_attr.value + farm_production_attr.value
            for farm_labour_action in farm_labour_actions:
                farm_labour_wealth_attr = farm_labour_action.initiator.attribute_values.get(attribute__exact='wealth')
                farm_labour_wealth_attr.value = F('value') + 1/labour_count*farm_labour_costs
                farm_labour_wealth_attr.save(update_fields=['value'])
            farm_owner_wealth_attr.value = 0
            farm_owner_wealth_attr.save(update_fields=['value'])

    #(Check if any players or labourers have died:)

    #Update all players' and labourers' leisure:
    labourers_who_didnt_work = GameInstanceObject.objects.filter(game_instance.id__exact=instance_id, game_object.game_object.arch_game_object__exact='labour', initiated_actions.turn__exact=turn, ~Q(initiated_actions.action__exact='work'))
    players_who_didnt_work = GameInstanceObject.objects.filter(game_instance.id__exact=instance_id, game_object.game_object.arch_game_object__exact='player', initiated_actions.turn__exact=turn, ~Q(initiated_actions.action__exact='work'))
    for labour in labourers_who_didnt_work:
        labour.enjoy_leisure()
    for player in players_who_didnt_work:
        player.enjoy_leisure()
    
    #Update turn no.
    turn = F('turn') + 1    
