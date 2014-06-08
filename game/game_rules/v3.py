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
    from game.models import GameInstanceObject, Action, ArchAttribute, GameInstanceObjectAttributeValue, ArchGameObject
    

    instance_id = instance.id
    turn = instance.turn
    nature = instance.game_instance_objects.all().get(
            game_instance__id=instance_id, 
            type__arch_game_object='nature'
            )
    governor = instance.game_instance_objects.all().get(
            game_instance__id=instance_id, 
            type__arch_game_object='governor'
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
    properties = instance.game_instance_objects.all().exclude(
            type__arch_game_object='player'
            ).exclude(
            type__arch_game_object='nature'
            ).exclude(
            type__arch_game_object='governor'
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
            own_wage_action = list(
                    player.initiated_actions.all().filter(
                        turn=turn,
                        action__arch_action='set_wage',
                        ).order_by('-parameters')[:1]
                    )[0]
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
        if float(farm_owner_wealth_attr.value) >= float(take_wage_action.parameters):
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
        if int(plot.attribute_values.all().get(attribute__arch_attribute='development_cost').value) <= 0:
            plot.attribute_values.all().get(attribute__arch_attribute='development_cost').delete()
            plot.attribute_values.all().get(attribute__arch_attribute='minimum_bid').delete()
            plot.relationship_objects.all().get(relationship__arch_relationship='develops').delete()
            plot.create_attribute('labour_spots', 2)
            plot.create_attribute('production', 0)
            farm_type_object = ArchGameObject.objects.get(arch_game_object='farm')
            plot.type = farm_type_object
            plot.save(update_fields=['type'])


    # If players bought unowned plots, assign based on who can set aside the most, at least the min_bid up to their bid value
    bid_unowned_plots = plots.filter(
            affected_by_actions__action__arch_action='bid_to_buy',
            affected_by_actions__turn=turn,
            ).exclude(
            relationship_objects__relationship__arch_relationship='owns'
            ).distinct()
    for plot in bid_unowned_plots:
        # Get set of bids whose values are less than the owner's wealth attr value
        ordered_bid_actions = plot.affected_by_actions.all().filter(
                action__arch_action='bid_to_buy',
                turn=turn
                ).order_by('-parameters')
        excluded_bids = []
        for bid_action in ordered_bid_actions:
            if float(bid_action.parameters) >= float(bid_action.initiator.attribute_values.all().get(attribute__arch_attribute='wealth').value):
                excluded_bids = excluded_bids + [bid_action]
            # Should move the next clause to form validation!! BUT only once instance passed through...
            elif float(bid_action.parameters) < float(plot.attribute_values.all().get(attribute__arch_attribute='minimum_bid').value):
                excluded_bids = excluded_bids + [bid_action]
        ordered_feasible_bid_actions = ordered_bid_actions.exclude(id__in=[bid.id for bid in excluded_bids])
        
        if ordered_feasible_bid_actions:
            highest_feasible_bid_action = ordered_feasible_bid_actions[0]
            highest_feasible_bidder = highest_feasible_bid_action.initiator
            plot_cost = float(highest_feasible_bid_action.parameters)
        
            bidder_wealth = highest_feasible_bidder.attribute_values.all().get(attribute__arch_attribute='wealth')
            bidder_wealth.value = F('value') - plot_cost
            bidder_wealth.save(update_fields=['value'])
        
            governor_wealth_attr = governor.attribute_values.all().get(attribute__arch_attribute='wealth')
            governor_wealth_attr.value = F('value') + plot_cost
            governor_wealth_attr.save(update_fields=['value'])
        
            highest_feasible_bidder.create_relationship('owns', highest_feasible_bid_action.affected)
            highest_feasible_bidder.create_relationship('develops', highest_feasible_bid_action.affected)


    # If any players have bid on selling properties, assign like above
    bid_properties = properties.filter(
            affected_by_actions__action__arch_action='bid_to_buy',
            affected_by_actions__turn=turn
            ).distinct()
    for property in bid_properties:
        # Get set of bids whose values are less than the owner's wealth attr value
        ordered_bid_actions = property.affected_by_actions.all().filter(
                action__arch_action='bid_to_buy',
                turn=turn
                ).order_by('-parameters')
        excluded_bids = []
        for bid_action in ordered_bid_actions:
            if float(bid_action.parameters) >= float(bid_action.initiator.attribute_values.all().get(attribute__arch_attribute='wealth').value):
                excluded_bids = excluded_bids + [bid_action]
            # Should move the next clause to form validation!! BUT only once instance passed through...
            elif float(bid_action.parameters) < float(property.attribute_values.all().get(attribute__arch_attribute='minimum_bid').value):
                excluded_bids = excluded_bids + [bid_action]
        ordered_feasible_bid_actions = ordered_bid_actions.exclude(id__in=[bid.id for bid in excluded_bids])
        
        if ordered_feasible_bid_actions:
            highest_feasible_bid_action = ordered_feasible_bid_actions[0]
            highest_feasible_bidder = highest_feasible_bid_action.initiator
            property_cost = float(highest_feasible_bid_action.parameters)
            seller = property.relationship_objects.all().get(relationship__arch_relationship='owns').subject_game_instance_object
        
            bidder_wealth = highest_feasible_bidder.attribute_values.all().get(attribute__arch_attribute='wealth')
            bidder_wealth.value = F('value') - property_cost
            bidder_wealth.save(update_fields=['value'])
        
            seller_wealth_attr = seller.attribute_values.all().get(attribute__arch_attribute='wealth')
            seller_wealth_attr.value = F('value') + property_cost
            seller_wealth_attr.save(update_fields=['value'])
        
            #Transfer all interests (relationships) in the property from the seller to the buyer
            for relationship in property.relationship_objects.all().filter(subject_game_instance_object=seller):
                relationship.subject_game_instance_object = highest_feasible_bidder
                relationship.save(update_fields=['subject_game_instance_object'])
            
            #Delete sale-specific attributes and relationships
            property.relationship_objects.all().get(relationship__arch_relationship='sells').delete()
            property.attribute_values.all().get(attribute__arch_attribute='minimum_bid').delete()
    

    # If any players have sold any properties, create that relationship
    new_properties_on_market = properties.filter(
            affected_by_actions__turn=turn,
            affected_by_actions__action__arch_action='sell',
            affected_by_actions__parameters='yes'
            )
    if new_properties_on_market:
        for property in new_properties_on_market:
            owner = property.affected_by_actions.all().get(
                    turn=turn,
                    action__arch_action='sell',
                    parameters='yes'
                    ).initiator
            owner.create_relationship('sells', property)
            property.create_attribute('minimum_bid',0)
    
    
    # If any players have reset their minimum bids, reset those bids!
    properties_with_reset_bids = properties.filter(
            affected_by_actions__turn=turn,
            affected_by_actions__action__arch_action='set_min_bid'
            )
    if properties_with_reset_bids:
        for property in properties_with_reset_bids:
            new_min_bid_action = property.affected_by_actions.all().get(
                    turn=turn,
                    action__arch_action='set_min_bid'
                    )
            min_bid_attr = property.attribute_values.all().get(attribute__arch_attribute='minimum_bid')
            min_bid_attr.value = float(new_min_bid_action.parameters)
            min_bid_attr.save(update_fields=['value'])  


    # If any players have taken their properties off the market, remove the sell relationship
    properties_taken_off_market = properties.filter(
            affected_by_actions__turn=turn,
            affected_by_actions__action__arch_action='take_off_market',
            affected_by_actions__parameters='yes'
            )
    if properties_taken_off_market:
        for property in properties_taken_off_market:
            property.attribute_values.all().get(attribute__arch_attribute='minimum_bid').delete()
            property.relationship_objects.all().get(relationship__arch_relationship='sells').delete()


    # If any players have died, set their wealth = 0:
    for player in players:
        if player.attribute_values.all().get(attribute__arch_attribute='wealth').value < 0:
            player.attribute_values.all().get(attribute__arch_attribute='wealth').value = 0
            player.attribute_values.all().get(attribute__arch_attribute='wealth').save(update_fields=['value'])
    

    # Update all living players' leisure:
    for player in living_players:
        if player not in working_players:
            enjoy_leisure(player)
    
    
    # Animate unborn
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
    
    for player in living_players:
        score_attr = player.attribute_values.all().get(attribute__arch_attribute='score')
        score_seed_attr = player.attribute_values.all().get(attribute__arch_attribute='score_seed')
        leisure_attr = player.attribute_values.all().get(attribute__arch_attribute='leisure')
        wealth_attr = player.attribute_values.all().get(attribute__arch_attribute='wealth')
        score_attr.value = (
                50 * 
                (float(wealth_attr.value) ** float(score_seed_attr.value)) *
                ((float(leisure_attr.value) + 0.5) ** (1 - float(score_seed_attr.value)))
                )
        score_attr.save(update_fields=['value'])
    