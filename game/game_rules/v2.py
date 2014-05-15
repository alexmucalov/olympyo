"""
*** Intended initial DB definition ***

*Arch_layout_type: display_object, autonomous_object, nature_object
*Arch_actions: work, take_wage, set_wage
*Arch_attribute_sets: normal_player, normal_labour, normal_farm
*Arch_attributes: productivity, labour_spots, labour_working, production, cost, leisure, wealth
*Arch_game_objects: player, labour, farm, nature
*Arch_game_object_attribute_values: [farm, labour_working, 0], [farm, labour_spots, 2], [farm, production, 0], [farm, productivity, 2], [farm, cost, 2], [player, leisure, 0], [player, wealth, 2], [labour, leisure, 0], [labour, wealth, 2]
*Arch_relationships: owns
*Game_object_attribute_values: as directly above, but with 'normal_' prepended to each game_object
*Game_object_sets: farm_village
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
#Remember get_or_create, here
#Use map, here
"""
# Instance method on GameInstance objects; ruleset is called dynamically
# Right now, functions imported from components are global; what about using inheritance 
# to extend GameInstanceObjects? E.g., class Player(GameInstanceObject)...
# and then defining the methods that apply to that class (e.g., eat) (which can themselves be drawn
# from components)? Would be much better, no? Then how to define existing GameInstanceObjects
# as members of new subclasses like Player? Instead of eat(labour), would have labour.eat()

def perform(instance):
    from random import *
    from decimal import *
    
    from django.db.models import Q, F
    from game.game_rules.components import eat, labour_worked, produce, enjoy_leisure
    from game.models import GameInstanceObject, Action
    

    instance_id = instance.id
    turn = instance.turn
    nature = GameInstanceObject.objects.get(
            game_instance__id=instance_id, 
            game_object__game_object__arch_game_object='nature'
            )
    
    
    # Record turn seed for reproducible randomness
    #Get seed as Decimal object, because Decimal has a method that effectively
    #Returns self (copy_abs) without taking any arguments:
    #Necessary to reproducibly seed random.shuffle
    seed = Decimal.from_float(round(random(),5))
    nature.act(action_name='set_seed', parameters=seed)


    # Define players and labourers
    players = GameInstanceObject.objects.filter(
            game_instance__id=instance_id, 
            game_object__game_object__arch_game_object='player'
            )
    labourers = GameInstanceObject.objects.filter(
            game_instance__id=instance_id, 
            game_object__game_object__arch_game_object='labour'
            )
    farms = GameInstanceObject.objects.filter(
            game_instance__id=instance_id, 
            game_object__game_object__arch_game_object='farm'
            )
    living_players = players.filter(
            attribute_values__attribute__arch_attribute='wealth', 
            attribute_values__value__gt=0
            )
    living_labourers = labourers.filter(
            attribute_values__attribute__arch_attribute='wealth', 
            attribute_values__value__gt=0
            )


    # Living players and living labourers eat 1 wealth:
    for player in living_players:
        eat(player)
    for labour in living_labourers:
        eat(labour)            
            
 
    # Have random living labour take action to take wages and work
    #Random work can be much more efficient - but not important yet
    #count_set_wage_actions = len(set_wage_actions)
    #count_labourers = len(labourers)
    #if count_labourers > count_set_wage_actions: #WRONG! Need to sample by seed, too
        #wage_winners = random.sample(labourers, count_set_wage_actions)
        #random.shuffle(wage_winners, seed)
    #else:
        #set_wage_actions = set_wage_actions.order_by('-parameters')
    set_wage_actions = Action.objects.filter(
            initiator__game_instance__id=instance_id, 
            turn=turn, action__arch_action='set_wage'
            ).order_by('-parameters')
    labourer_l = list(living_labourers)
    shuffle(labourer_l, seed.copy_abs)
    labour_and_wages_offered = zip(labourer_l, set_wage_actions)
    
    for (labour, wage_offered) in labour_and_wages_offered:
        labour.act(
                action_name='take_wage', 
                parameters=wage_offered.parameters, 
                affected_id=wage_offered.affected.id
                )
        labour.act(
                action_name='work', 
                parameters='yes', 
                affected_id=wage_offered.affected.id
                )
    
    # Farm increases labour_working for everyone working it:
    worked_farms = farms.filter(
            game_instance__turn=turn, 
            affected_by_actions__action__arch_action='work', 
            affected_by_actions__parameters='yes'
            ).distinct()

    for farm in worked_farms:
        labour_worked(farm)

    # Farms produce based on total labour_working, 
    # then split production between wages and profits:
    for farm in farms:
        produce(farm)
        
        # Split production only if farm is owned
        try:
            farm_owner = farm.relationship_objects.all().get(
                    relationship__arch_relationship='owns'
            ).subject_game_instance_object
        except:
            continue
        
        # Common source values
        farm_production_attr = farm.attribute_values.all().get(
                attribute__arch_attribute='production'
                )
        farm_owner_wealth_attr = farm_owner.attribute_values.all().get(
                attribute__arch_attribute='wealth'
                )
        farm_take_wage_actions = farm.affected_by_actions.all().filter(
                action__arch_action='take_wage', 
                turn=turn
                )
        labour_count = len(farm_take_wage_actions)
        farm_wages_offered = []
        for farm_take_wage_action in farm_take_wage_actions:
            farm_wage_offered = [float(farm_take_wage_action.parameters)]
            farm_wages_offered = farm_wages_offered + farm_wage_offered
        
        # If owner can pay all costs, do so, then keep the rest
        if (float(farm_owner_wealth_attr.value) + float(farm_production_attr.value) >= 
                    sum(farm_wages_offered)):
            farm_labour_costs = 0
            for farm_take_wage_action in farm_take_wage_actions:
                farm_wage_offered = float(farm_take_wage_action.parameters)
                farm_labour_costs += farm_wage_offered
                farm_labour_wealth_attr = farm_take_wage_action.initiator.attribute_values.all().get(
                        attribute__arch_attribute='wealth'
                        )
                farm_labour_wealth_attr.value = F('value') + farm_wage_offered
                farm_labour_wealth_attr.save(update_fields=['value'])
            farm_owner_wealth_attr.value = (
                    F('value') + 
                    float(farm_production_attr.value) - 
                    farm_labour_costs
                    )
            farm_owner_wealth_attr.save(update_fields=['value'])
        
        # If owner can't pay all the costs, pay as much as possible evenly 
        # among all labourers, then set owner wealth = 0
        else:
            farm_labour_costs = (
                    float(farm_owner_wealth_attr.value) + 
                    float(farm_production_attr.value)
                    )
            for farm_take_wage_action in farm_take_wage_actions:
                farm_labour_wealth_attr = farm_take_wage_action.initiator.attribute_values.all().get(
                        attribute__arch_attribute='wealth'
                        )
                farm_labour_wealth_attr.value = (
                        F('value') + 
                        1/labour_count*farm_labour_costs
                        )
                farm_labour_wealth_attr.save(update_fields=['value'])
            farm_owner_wealth_attr.value = 0
            farm_owner_wealth_attr.save(update_fields=['value'])
        
    # If players bought unowned farms, deduct costs 
    # and assign farms on first-come, first-served basis
    for player in living_players:
        player_purchases = player.initiated_actions.all().filter(
                turn=turn,
                action__arch_action='buy',
                )
        owned_objects = instance.game_instance_objects.all().filter(
                relationship_objects__relationship__arch_relationship='owns',
                relationship_objects__object_game_instance_object__isnull=False,
                )
        if player_purchases:
            for purchase in player_purchases:
                if purchase.affected in owned_objects:
                    continue
                else:
                    farm_cost = purchase.affected.attribute_values.all().get(attribute__arch_attribute='cost').value
                    player_wealth = player.attribute_values.all().get(attribute__arch_attribute='wealth')
                    player_wealth.value = F('value') - farm_cost
                    player_wealth.save(update_fields=['value'])
                    player.create_relationship('owns', purchase.affected)

    #If any players or labourers have died, then set their wealth = 0:
    for player in living_players:
        if player.attribute_values.all().get(attribute__arch_attribute='wealth').value < 0:
            player.attribute_values.all().get(attribute__arch_attribute='wealth').value = 0
            player.attribute_values.all().get(attribute__arch_attribute='wealth').save(update_fields=['value'])
    
    for labourer in living_labourers:
        if labourer.attribute_values.all().get(attribute__arch_attribute='wealth').value < 0:
            labourer.attribute_values.all().get(attribute__arch_attribute='wealth').value = 0
            labourer.attribute_values.all().get(attribute__arch_attribute='wealth').save(update_fields=['value'])

    #Update all players' and labourers' leisure:
    labourers_who_didnt_work = living_labourers.filter(
            initiated_actions__action__arch_action='work', 
            initiated_actions__parameters='no', 
            initiated_actions__turn=turn
            ).distinct()
    for labour in labourers_who_didnt_work:
        enjoy_leisure(labour)
    for player in living_players:
        enjoy_leisure(player)