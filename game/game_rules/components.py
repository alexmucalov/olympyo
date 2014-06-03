"""
Component game functions
* Define by rule_set that function applies to
* And by the game_objects to which the function applies
"""
from django.db.models import Q, F

#v1 - applies to players and labourers
def eat(living_object):
    living_object_wealth_attr = living_object.attribute_values.all().get(attribute__arch_attribute='wealth')
    living_object_wealth_attr.value = F('value') - 1
    living_object_wealth_attr.save(update_fields=['value'])


#v1 - applies to all farms
def labour_worked(farm):
    turn = farm.game_instance.turn
    labour_working = farm.affected_by_actions.all().filter(turn=turn, action__arch_action='take_wage').count()
    labour_working_attr = farm.attribute_values.all().get(attribute__arch_attribute='labour_working')
    labour_working_attr.value = labour_working
    labour_working_attr.save(update_fields=['value'])


#v1 - applies to all farms
def produce(farm):
    production_attr = farm.attribute_values.all().get(attribute__arch_attribute='production')
    labour_working_attr = farm.attribute_values.all().get(attribute__arch_attribute='labour_working')
    productivity_attr = farm.attribute_values.all().get(attribute__arch_attribute='productivity')
    production_attr.value = float(labour_working_attr.value) ** float(productivity_attr.value)
    production_attr.save(update_fields=['value'])


def develop(plot):
    dev_cost_attr = plot.attribute_values.all().get(attribute__arch_attribute='development_cost')
    labour_working_attr = plot.attribute_values.all().get(attribute__arch_attribute='labour_working')
    dev_cost_attr.value = F('value') - float(labour_working_attr.value)
    dev_cost_attr.save(update_fields=['value'])


#v1 - applies to players and labourers who didn't work
def enjoy_leisure(living_object):    
    leisure_attr = living_object.attribute_values.all().get(attribute__arch_attribute='leisure')
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