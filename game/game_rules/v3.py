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
    from game.game_rules.components import eat, labour_worked, produce, enjoy_leisure, develop
    from game.models import GameInstanceObject, Action
    

    instance_id = instance.id
    turn = instance.turn
    nature = instance.game_instance_objects.all().get(
            game_instance__id=instance_id, 
            type__arch_game_object='nature'
            )
    
    
    # Record turn seed for reproducible randomness
    #Get seed as Decimal object, because Decimal has a method that effectively
    #Returns self (copy_abs) without taking any arguments:
    #Necessary to reproducibly seed random.shuffle
    seed = Decimal.from_float(round(random(),5))
    nature.act(action_name='set_seed', parameters=seed)


    # Define players and labourers
    players = instance.game_instance_objects.all().filter(
            game_instance__id=instance_id, 
            type__arch_game_object='player'
            )
    living_players = players.filter(
            attribute_values__attribute__arch_attribute='wealth', 
            attribute_values__value__gt=0
            )
    working_players = living_players.filter(
            initiated_actions__action__arch_action='work',
            initiated_actions__parameters='yes',
            initiated_actions__turn=turn
            ).distinct()
    farms = instance.game_instance_objects.all().filter(
            game_instance__id=instance_id, 
            type__arch_game_object='farm'
            )
    plots = instance.game_instance_objects.all().filter(
            game_instance__id=instance_id, 
            type__arch_game_object='plot'
            )


    # Living players eat 1 wealth:
    for player in living_players:
        eat(player)           


    # Have players who work AND own their own properties take the highest wage that they set
    landed_working_players = working_players.filter(
            relationship_subjects__subject_game_instance_object__isnull=False
            ).distinct()
    wage_offerors = living_players.filter(
            initiated_actions__turn=turn,
            initiated_actions__action__arch_action='set_wage'
            ).distinct()
    own_set_wage_actions = []
    own_wage_working_players = []
    for player in landed_working_players:
        if player in wage_offerors:
            own_wage_action = player.initiated_actions.all().filter(
                    turn=turn,
                    action__arch_action='set_wage',
                    ).order_by('-parameters')[:1]
            player.act(
                    action_name='take_wage',
                    parameters=own_wage_action.parameters,
                    affected_id=own_wage_action.affected.id
                    )
            own_set_wage_actions = own_set_wage_actions + [own_wage_action]
            own_wage_working_players = own_wage_working_players + [player]


    # Have remaining working_players randomly take action to take remaining wages and work
    #Random work can be much more efficient - but not important yet
    #count_set_wage_actions = len(set_wage_actions)
    #count_labourers = len(labourers)
    #if count_labourers > count_set_wage_actions: #WRONG! Need to sample by seed, too
        #wage_winners = random.sample(labourers, count_set_wage_actions)
        #random.shuffle(wage_winners, seed)
    #else:
        #set_wage_actions = set_wage_actions.order_by('-parameters')
    all_set_wage_actions = Action.objects.filter(
            initiator__game_instance=instance, 
            turn=turn, 
            action__arch_action='set_wage'
            ).order_by('-parameters')
    remaining_set_wage_actions = [action for action in all_set_wage_actions if action not in own_set_wage_actions]
    remaining_working_players = [player for player in working_players if player not in own_wage_working_players]
    shuffle(remaining_working_players, seed.copy_abs)
    labour_and_wages_offered = zip(remaining_working_players, remaining_set_wage_actions)
    
    for (working_player, wage_offered) in labour_and_wages_offered:
        working_player.act(
                action_name='take_wage', 
                parameters=wage_offered.parameters, 
                affected_id=wage_offered.affected.id
                )

    
    # Farm increases labour_working for everyone taking a wage on it:
    owned_farms = farms.filter(relationship_objects__relationship__arch_relationship='owns').distinct()
    for farm in owned_farms:
        labour_worked(farm)

        # Farms produce based on total labour_working, and return product to farm owners
        produce(farm)
        farm_production_attr = farm.attribute_values.all().get(
                attribute__arch_attribute='production'
                )
        farm_owner = farm.relationship_objects.all().get(
                relationship__arch_relationship='owns'
                ).subject_game_instance_object
        farm_owner_wealth_attr = farm_owner.attribute_values.all().get(
                attribute__arch_attribute='wealth'
                )
        farm_owner_wealth_attr.value = F('value') + float(farm_production_attr.value)
        farm_owner_wealth_attr.save(update_fields=['value'])
    
    
    # Owners pay people working farms that turn, if affordable
    take_wage_actions = Action.objects.filter(
            initiator__game_instance=instance,
            action__arch_action='take_wage', 
            turn=turn
            )
    for take_wage_action in take_wage_actions:
        farm_labourer = take_wage_action.initiator
        farm_labourer_wealth_attr = farm_labourer.attribute_values.all().get(
                attribute__arch_attribute='wealth'
                )
        farm_owner = take_wage_action.affected.relationship_objects.all().get(
                relationship__arch_relationship='owns'
                ).subject_game_instance_object
        farm_owner_wealth_attr = farm_owner.attribute_values.all().get(
                attribute__arch_attribute='wealth'
                )
        if (float(farm_owner_wealth_attr.value) >= float(take_wage_action.parameters):
            farm_labourer_wealth_attr.value = F('value') + float(take_wage_action.parameters)
            farm_labourer_wealth_attr.save(update_fields=['value'])
            farm_owner_wealth_attr.value = F('value') - float(take_wage_action.parameters)
            farm_owner_wealth_attr.save(update_fields=['value'])
        else:
            farm_labourer_wealth_attr.value = F('value') + float(farm_owner_wealth_attr.value)
            farm_labourer_wealth_attr.save(update_fields=['value'])
            farm_owner_wealth_attr.value = 0
            farm_owner_wealth_attr.save(update_fields=['value'])
            

    # Develop plots; then turn plots into farms once developed
    owned_plots = plots.filter(
            relationship_objects__relationship__arch_relationship='owns'
            ).distinct()
    for plot in owned_plots:
        labour_worked(plot)
        develop(plot)
        if plot.attribute_values.all().get(attribute_values__attribute__arch_attribute='development_cost').value <= 0:
            plot.attribute_values.all().get(attribute_values__attribute__arch_attribute='development_cost').delete()
            plot.attribute_values.all().get(attribute_values__attribute__arch_attribute='min_bid').delete()
            plot.relationship_objects.all().get(relationship__arch_relationship='develops').delete()
            labour_spots_arch_attr = ArchAttribute.objects.get(arch_attribute='labour_spots')
            production_arch_attr = ArchAttribute.objects.get(arch_attribute='production')
            GameInstanceObjectAttributeValue.objects.create_game_instance_object_attribute_value(game_instance_object=plot, attribute=labour_spots_arch_attr, value=2)
            GameInstanceObjectAttributeValue.objects.create_game_instance_object_attribute_value(game_instance_object=plot, attribute=production_arch_attr, value=0)
            farm_type_object = ArchGameObject.objects.get(arch_game_object='farm')
            plot.type = farm_type_object
            plot.save(update_fields=['type'])


    # If players bought unowned plots, assign based on who can set aside the most, at least the min_bid up to their bid value
    bid_plots = plots.filter(
            affected_by_actions__action__arch_action='bid',
            turn=turn
            ).distinct()
    for plot in bid_plots:
        # Get set of bids whose values are less than the owner's wealth attr value
        ordered_bid_actions = plot.affected_by_actions.all().filter(
                affected_by_actions__action__arch_action='bid',
                turn=turn
                ).order_by('-parameters')
        for bid_action in ordered_bid_actions:
            if float(bid_action.parameters) >= float(bid_action.initiator.attribute_values.all().get(attribute__arch_attribute='wealth').value):
                bid_action.delete()
            # Should move the next clause to form validation!! BUT only once instance passed through...
            if float(bid_action.parameters) < float(plot.attribute_values.all().get(attribute__arch_attribute='min_bid').value):
                bid_action.delete()
        
        highest_feasible_bid_action = ordered_bid_actions[0]
        highest_feasible_bidder = highest_feasible_bid_action.initiatior
        plot_cost = highest_feasible_bid_action.parameters
        
        bidder_wealth = highest_feasible_bidder.attribute_values.all().get(attribute__arch_attribute='wealth')
        bidder_wealth.value = F('value') - plot_cost
        bidder_wealth.save(update_fields=['value'])
        
        plot_dev_fund = plot.attribute_values.all().get(attribute__arch_attribute='development_fund')
        plot_dev_fund.value = plot_cost
        plot_dev_fund.save(update_fields=['value'])
        
        highest_feasible_bidder.create_relationship('owns', highest_feasible_bid_action.affected)


    #If any players have died, set their wealth = 0:
    for player in players:
        if player.attribute_values.all().get(attribute__arch_attribute='wealth').value < 0:
            player.attribute_values.all().get(attribute__arch_attribute='wealth').value = 0
            player.attribute_values.all().get(attribute__arch_attribute='wealth').save(update_fields=['value'])
    

    #Update all living players' leisure:
    for player in living_players:
        if player not in working_players:
            enjoy_leisure(player)
    
    
    #Animate unborn
    animate_actions = nature.initiated_actions.all().filter(
            action__arch_action='animate',
            turn=turn)
    if animate_actions.exists():
        for action in animate_actions:
            newborn = action.affected
            newborn_wealth_attr = newborn.attribute_values.all().get(
                    attribute__arch_attribute='wealth'
                    )
            newborn_wealth_attr.value = action.parameters
            newborn_wealth_attr.save(update_fields=['value'])