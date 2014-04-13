"""
Component game functions
* Define by rule_set that function applies to
* And by the game_objects to which the function applies
"""
from django.db.models import Q, F

#v1 - applies to players and labourers
def eat(living_object):
    living_object_wealth_attr = living_object.attribute_values.all().get(attribute__arch_attribute="wealth")
    living_object_wealth_attr.value = F('value') - 1
    living_object_wealth_attr.save(update_fields=['value'])


#v1 - applies to farms
def reset_labour_working(farm):
    labour_working_attr = farm.attribute_values.all().get(attribute__arch_attribute="labour_working")
    labour_working_attr.value = 0
    labour_working_attr.save(update_fields=['value'])


#v1 - applies to players who own a single farm
def work_own_farm(living_object):
    player_farm = living_object.relationship_subjects.all().get(relationship__arch_relationship="owns").object_game_instance_object
    labour_working_attr = player_farm.attribute_values.all().get(attribute__arch_attribute="labour_working")
    labour_working_attr.value = F('value') + 1
    labour_working_attr.save(update_fields=['value'])



#v1 - applies to all farms
def labour_worked(farm):
    count_set_wage_actions = farm.affected_by_actions.all().filter(action__arch_action="set_wage").count()
    count_take_wage_actions = farm.affected_by_actions.all().filter(action__arch_action="take_wage").count()
    labour_working = min(count_set_wage_actions, count_take_wage_actions)
    labour_working_attr = farm.attribute_values.all().get(attribute__arch_attribute="labour_working")
    labour_working_attr.value = F('value') + labour_working
    labour_working_attr.save(update_fields=['value'])


#v1 - applies to all farms
def produce(farm):
    production_attr = farm.attribute_values.all().get(attribute__arch_attribute="production")
    labour_working_attr = farm.attribute_values.all().get(attribute__arch_attribute="labour_working")
    productivity_attr = farm.attribute_values.all().get(attribute__arch_attribute="productivity")
    production_attr.value = float(labour_working_attr.value) ** float(productivity_attr.value)
    production_attr.save(update_fields=['value'])


#v1 - applies to players and labourers who didn't work
def enjoy_leisure(living_object):    
    leisure_attr = living_object.attribute_values.all().get(attribute__arch_attribute="leisure")
    leisure_attr.value = F('value') + 1
    leisure_attr.save(update_fields = ['value'])


#v1 - applies to labourers who work
#def earn(self):
    #labourer_wealth_attr = self.attribute_values.get(attribute='wealth')
    #labourer_wealth_attr.value = F('value') + wage_offered.parameters
    #labourer_wealth_attr.save(update_fields=['value'])

#v1 - applies to players who own farms
#def profit(self):
    #pass