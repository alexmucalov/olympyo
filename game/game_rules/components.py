"""
Component game functions
* Define by rule_set that function applies to
* And by the game_objects to which the function applies
"""

#v1 - applies to players and labourers
def eat(self):
    living_object_wealth_attr = self.attribute_values.get(attribute__exact='wealth')
    living_object_wealth_attr.value = F('value') - 1
    living_object_wealth_attr.save(update_fields=['value'])


#v1 - applies to farms
def reset_labour_working(self):
    labour_working_attr = self.attribute_values.get(attribute='labour_working')
    labour_working_attr.value = 0
    labour_working_attr.save(update_fields=['value'])


#v1 - applies to players who own a single farm
def work_own_farm(self):
    player_farm = self.relationship_subjects.get(relationship.arch_relationship='owns').object_game_instance_object
    labour_working_attr = player_farm.attribute_values.get(attribute='labour_working')
    labour_working_attr.value = F('value') + 1
    labour_working_attr.save(update_fields=['value'])



#v1 - applies to all farms
def labour_worked(self):
    count_set_wage_actions = self.affected_by_actions.filter(action.arch_action__exact='set_wage').count()
    count_take_wage_actions = self.affected_by_actions.filter(action.arch_action__exact='take_wage').count()
    labour_working = min(count_set_wage_actions, count_take_wage_actions)
    labour_working_attr = self.attribute_values.get(attribute__exact='labour_working')
    labour_working_attr.value = F('value') + labour_working
    labour_working_attr.save(update_fields=['value'])


#v1 - applies to all farms
def produce(self):
    production_attr = self.attribute_values.get(attribute__exact='production')
    labour_working_attr = self.attribute_values.get(attribute__exact='labour_working')
    productivity_attr = self.attribute_values.get(attribute__exact='productivity')
    production_attr.value = labour_working_attr.value ** productivity_attr.value
    production_attr.save(update_fields=['value'])


#v1 - applies to players and labourers who didn't work
def enjoy_leisure(self):    
    leisure_attr = self.attribute_values.get(attribute__exact='leisure')
    leisure_attr.value = F('value') + 1
    leisure_attr.save(update_fields = ['value'])


#v1 - applies to labourers who work
def earn(self):
    labourer_wealth_attr = self.attribute_values.get(attribute__exact='wealth')
    labourer_wealth_attr.value = F('value') + wage_offered.parameters
    labourer_wealth_attr.save(update_fields=['value'])

#v1 - applies to players who own farms
def profit(self):
    pass