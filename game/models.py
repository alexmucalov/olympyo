from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F

from random import *


# Game Rules Models
class GameRuleManager(models.Manager):
    def create_game_rule(self, game_rules):
        game_rules = self.create(game_rules=game_rules)
        return game_rules


class GameRule(models.Model):
    game_rules = models.CharField(max_length=30)
    #Should be called a ruleset, not rules; then, later, rulesets can be composed of rules

    objects = GameRuleManager()

    class Meta:
        unique_together = ('game_rules',)

    def __unicode__(self):
        return u'%s' % (self.game_rules)



# Archetype Models
class ArchLayoutType(models.Model):
    arch_layout = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ('arch_layout',)    

    def __unicode__(self):
        return u'%s' % (self.arch_layout)


class ArchDisplayRulesetManager(models.Manager):
    def create_arch_display_ruleset(self, arch_display_ruleset):
        arch_display_ruleset = self.create(arch_display_ruleset=arch_display_ruleset)
        return arch_display_ruleset


class ArchDisplayRuleset(models.Model):
    arch_display_ruleset = models.CharField(max_length=255)
    
    objects = ArchDisplayRulesetManager()
    
    class Meta:
        unique_together = ('arch_display_ruleset',)
    
    def __unicode__(self):
        return u'%s' % (self.arch_display_ruleset)


class ArchAction(models.Model):
    arch_action = models.CharField(max_length=255)

    class Meta:
        unique_together = ('arch_action',)

    def __unicode__(self):
        return u'%s' % (self.arch_action)


class ArchAttribute(models.Model):
    arch_attribute = models.CharField(max_length=255)

    class Meta:
        unique_together = ('arch_attribute',)

    def __unicode__(self):
        return u'%s' % (self.arch_attribute.replace('_',' '))


class ArchGameObject(models.Model):
    arch_game_object = models.CharField(max_length=255)
    layout_type = models.ForeignKey(ArchLayoutType)

    class Meta:
        unique_together = ('arch_game_object',)

    def __unicode__(self):
        return u'%s' % (self.arch_game_object)


class ArchAttributeSet(models.Model):
    attribute_set = models.CharField(max_length=255)
    #game_object = models.ForeignKey(ArchGameObject)
    # Might need game_object to add extra validation - when adding attribute_set
    # to GameObject, check that game_object fields in both models match

    class Meta:
        unique_together = ('attribute_set',)

    def __unicode__(self):
        return u'%s' % (self.attribute_set.replace('_',' '))


class ActionPermissionSetManager(models.Manager):
    def action_permission_set(self, action_permission_set):
        action_permission_set = self.create(action_permission_set=action_permission_set)
        return action_permission_set


class ActionPermissionSet(models.Model):
    action_permission_set = models.CharField(max_length=255)
    
    objects = ActionPermissionSetManager()
    
    class Meta:
        unique_together = ('action_permission_set',)
    
    def __unicode__(self):
        return u'%s' % self.action_permission_set


class ExoActionSet(models.Model):
    exo_action_set = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ('exo_action_set',)
    
    def __unicode__(self):
        return u'%s' % self.exo_action_set


class ArchGameObjectAttributeValue(models.Model):
    arch_game_object = models.ForeignKey(ArchGameObject)
    attribute = models.ForeignKey(ArchAttribute)
    default_value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('arch_game_object','attribute')

    def __unicode__(self):
        return u'%s: %s' % (self.arch_game_object, self.attribute)


class ArchRelationship(models.Model):
    arch_relationship = models.CharField(max_length=255)

    class Meta:
        unique_together = ('arch_relationship',)

    def __unicode__(self):
        return u'%s' % self.arch_relationship


# Game Template Models
class GameObjectSetManager(models.Manager):
    def create_game_object_set(self, game_object_set):
        game_object_set = self.create(game_object_set=game_object_set)
        return game_object_set

class GameObjectSet(models.Model):
    game_object_set = models.CharField(max_length=255)
    
    objects = GameObjectSetManager()
    
    class Meta:
        unique_together = ('game_object_set',)
    
    def __unicode__(self):
        return u'%s' % self.game_object_set


class GameObjectRelationshipSetManager(models.Manager):
    def create_game_object_relationship_set(self, game_object_relationship_set):
        game_object_relationship_set = self.create(game_object_relationship_set=game_object_relationship_set)
        return game_object_relationship_set


class GameObjectRelationshipSet(models.Model):
    game_object_relationship_set = models.CharField(max_length=255)
    #game_object_set = models.ForeignKey(GameObjectSet)
    # Might need game_object_set to add extra validation - when adding game_object_relationship_set
    # to Game, check that game_object_set fields in both models match
    
    objects = GameObjectRelationshipSetManager()
        
    def __unicode__(self):
        return u'%s' % self.game_object_relationship_set


class GameObjectManager(models.Manager):
    def create_game_object(self, game_object_set, game_object, attribute_set):
        game_object = self.create(game_object_set=game_object_set, game_object=game_object, attribute_set=attribute_set)
        return game_object


class GameObject(models.Model):
    game_object_set = models.ForeignKey(GameObjectSet, related_name='game_objects')
    game_object = models.ForeignKey(ArchGameObject, related_name='game_objects')
    attribute_set = models.ForeignKey(ArchAttributeSet, related_name='game_objects', blank=True, null=True)
    # Ideally, game_object would determine attribute_sets available...
    
    objects = GameObjectManager()

    def __unicode__(self):
        return u'%s: id=%s' % (self.game_object, self.id)

    def create_instance_object(self, game_instance, user=None):
        game_object = self
        instance_object = GameInstanceObject.objects.create_game_instance_object(game_instance=game_instance, game_object=game_object, type=game_object.game_object, user=user)
        return instance_object


class GameObjectRelationshipManager(models.Manager):
    def create_game_object_relationship(self, relationship_set, subject_game_object, relationship, object_game_object):
        game_object_relationship = self.create(relationship_set=relationship_set, subject_game_object=subject_game_object, relationship=relationship, object_game_object=object_game_object)
        return game_object_relationship


class GameObjectRelationship(models.Model):
    relationship_set = models.ForeignKey(GameObjectRelationshipSet, related_name='relationships')
    subject_game_object = models.ForeignKey(GameObject, related_name='relationship_subjects')
    relationship = models.ForeignKey(ArchRelationship, related_name='relationships')
    object_game_object = models.ForeignKey(GameObject, related_name='relationship_objects')

    objects = GameObjectRelationshipManager()

    class Meta:
        unique_together = ('relationship_set','subject_game_object','relationship','object_game_object',)

    def __unicode__(self):
        return u'id=%s' % self.id

    def create_instance_object_relationship(self, game_instance):
        subject_game_instance_object = self.subject_game_object.game_instance_objects.all().get(game_instance=game_instance)
        relationship = self.relationship
        object_game_instance_object = self.object_game_object.game_instance_objects.all().get(game_instance=game_instance)
        instance_object_relationship = GameInstanceObjectRelationship.objects.create_game_instance_object_relationship(game_instance=game_instance, subject_game_instance_object=subject_game_instance_object, relationship=relationship, object_game_instance_object=object_game_instance_object)
        return instance_object_relationship


class GameObjectAttributeValue(models.Model):
    attribute_set = models.ForeignKey(ArchAttributeSet, related_name='attribute_values')
    attribute = models.ForeignKey(ArchAttribute)
    value = models.CharField(max_length = 255)
    # Ideally would be defined and available for a given game_object_type, and no other
    
    class Meta:
        unique_together = ('attribute_set','attribute')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.attribute_set, self.attribute, self.value)

    def create_instance_attribute_value(self, game_instance_object):
        attribute = self.attribute
        value = self.value
        attribute_set = self.attribute_set
        instance_attribute_value = GameInstanceObjectAttributeValue.objects.create_game_instance_object_attribute_value(game_instance_object=game_instance_object, attribute=attribute, value=value)
        return instance_attribute_value


class GameManager(models.Manager):
# Use ModelForm to give users the option to create games out of pre-specified objects!
# http://stackoverflow.com/questions/13285032/using-django-form-subclass-to-create-a-dropdown-list
    def create_game(self, name, game_object_set, game_object_relationship_set, game_rules, display_ruleset, action_permission_set, turns):
        game = self.create(name=name, game_object_set=game_object_set, game_rules=game_rules, display_ruleset=display_ruleset, action_permission_set=action_permission_set, turns=turns)
        return game


class Game(models.Model):
    name = models.CharField(max_length=255)
    game_object_set = models.ForeignKey(GameObjectSet, related_name='games')
    game_object_relationship_set = models.ForeignKey(GameObjectRelationshipSet, related_name='games')
    game_rules = models.ForeignKey(GameRule, related_name='games')
    display_ruleset = models.ForeignKey(ArchDisplayRuleset, related_name='games')
    action_permission_set = models.ForeignKey(ActionPermissionSet, related_name='games')
    exo_action_set = models.ForeignKey(ExoActionSet, related_name='games', blank=True, null=True)
    turns = models.IntegerField()
    
    objects = GameManager()

    class Meta:
        unique_together = (('game_object_set','game_object_relationship_set','game_rules','display_ruleset','action_permission_set','exo_action_set',),('name',),)

    def __unicode__(self):
        return u'%s' % (self.name.replace('_',' '))

    def create_instance(self):
        instance = GameInstance.objects.create_game_instance(game=self, turn=1)
        return instance
    
    def create_all_instance_objects(self, users):
        game_instance = self.create_instance()
        i = 0
        for game_object in self.game_object_set.game_objects.all():
            if game_object.game_object.arch_game_object == 'player':
                game_object_user = users[i]
                i += 1
            else:
                game_object_user = None
            game_instance_object = game_object.create_instance_object(game_instance=game_instance, user=game_object_user)
            if game_object.attribute_set:
                for attribute_value in game_object.attribute_set.attribute_values.all():
                    game_instance_object_attribute_value = attribute_value.create_instance_attribute_value(game_instance_object)
        for relationship in self.game_object_relationship_set.relationships.all():
            relationship.create_instance_object_relationship(game_instance)
        if self.exo_action_set:
            for action in self.exo_action_set.exo_actions.all():
                action.create_instance_exo_action(game_instance)


class WaitroomManager(models.Manager):
    def create_waitroom(self, game, users=None):
        waitroom = Waitroom(game=game)
        waitroom.save()
        waitroom.users.add(users)
        return waitroom
   

class Waitroom(models.Model):
    game = models.ForeignKey(Game, related_name='waitrooms')
    users = models.ManyToManyField(User, related_name='waitrooms')
    
    objects = WaitroomManager()
	
    def __unicode__(self):
        return u'%s' % (self.id)

    def add_user(self, user):
        if user not in self.users.all():
            self.users.add(user)
        users = self.users.all()
        user_count = users.count()
        game_player_count = self.game.game_object_set.game_objects.all().filter(
                game_object__arch_game_object='player'
                ).count()
        if user_count >= game_player_count:
        #    Send users to /game/, using nodejs or Python Twisted
            shuffle(list(users))
            self.game.create_all_instance_objects(users)
            self.delete()
    
    def remove_user(self, user):
        self.users.remove(user)
        user_count = self.users.all().count()
        if user_count == 0:
            self.delete()


# Game Instance Models
class GameInstanceManager(models.Manager):
    def create_game_instance(self, game, turn):
        game_instance = self.create(game=game, turn=turn)
        return game_instance


class GameInstance(models.Model):
    game = models.ForeignKey(Game)
    turn = models.IntegerField()
    
    objects = GameInstanceManager()
    
    def __unicode__(self):
        return u'%s: instance id=%s' % (self.game, self.id)
    
    def update_turn(self):
        ruleset = self.game.game_rules.game_rules
        exec "from game.game_rules.%s import perform" % ruleset
        perform(self)
        self.turn = F('turn') + 1
        self.save(update_fields=['turn'])
        


class GameInstanceObjectManager(models.Manager):
    def create_game_instance_object(self, game_instance, game_object, type, user=None):
        game_instance_object = self.create(game_instance=game_instance, game_object=game_object, type=type, user=user)
        return game_instance_object


class GameInstanceObject(models.Model):
    game_instance = models.ForeignKey(GameInstance, related_name='game_instance_objects')
    game_object = models.ForeignKey(GameObject, related_name='game_instance_objects')
    type = models.ForeignKey(ArchGameObject, related_name='game_instance_objects')
    user = models.ForeignKey(User, related_name='game_instance_objects', blank=True, null=True)
    
    objects = GameInstanceObjectManager()
	
    class Meta:
	    unique_together = ('game_instance','game_object')
	    get_latest_by = "id"

    def __unicode__(self):
        return u'%s: instance id=%s' % (self.game_object, self.id)

    def act(self, action_name, parameters=None, affected_id=None):
        action = ArchAction.objects.get(arch_action=action_name)
        turn = self.game_instance.turn
        if affected_id is None:
            affected = None
        else:
            affected = GameInstanceObject.objects.get(id=affected_id)
        Action.objects.create_action(turn=turn, initiator=self, action=action, parameters=parameters, affected=affected)
    
    def create_relationship(self, relationship_name, object_game_instance_object):
        relationship = ArchRelationship.objects.get(arch_relationship=relationship_name)
        GameInstanceObjectRelationship.objects.create_game_instance_object_relationship(
                game_instance=self.game_instance,
                subject_game_instance_object=self,
                relationship=relationship,
                object_game_instance_object=object_game_instance_object,
                )
    
    def create_attribute(self, attribute_name, value):
        attribute = ArchAttribute.objects.get(arch_attribute=attribute_name)
        GameInstanceObjectAttributeValue.objects.create_game_instance_object_attribute_value(
                game_instance_object=self, 
                attribute=attribute, 
                value=value
                )


class GameInstanceObjectAttributeValueManager(models.Manager):
    def create_game_instance_object_attribute_value(self, game_instance_object, attribute, value):
        attribute_value = self.create(game_instance_object=game_instance_object, attribute=attribute, value=value)
        return attribute_value


class GameInstanceObjectAttributeValue(models.Model):
    game_instance_object = models.ForeignKey(GameInstanceObject, related_name='attribute_values')
    attribute = models.ForeignKey(ArchAttribute)
    value = models.CharField(max_length=255)

    objects = GameInstanceObjectAttributeValueManager()

    class Meta:
        unique_together = ('game_instance_object','attribute')

    def __unicode__(self):
        return u'%s' % (self.attribute)


class GameInstanceObjectRelationshipManager(models.Manager):
    def create_game_instance_object_relationship(self, game_instance, subject_game_instance_object, relationship, object_game_instance_object):
        relationship = self.create(game_instance=game_instance, subject_game_instance_object=subject_game_instance_object, relationship=relationship, object_game_instance_object=object_game_instance_object)
        return relationship


class GameInstanceObjectRelationship(models.Model):
    game_instance = models.ForeignKey(GameInstance, related_name='relationships')
    subject_game_instance_object = models.ForeignKey(GameInstanceObject, related_name='relationship_subjects')
    relationship = models.ForeignKey(ArchRelationship, related_name='instance_relationships')
    object_game_instance_object = models.ForeignKey(GameInstanceObject, related_name='relationship_objects')
    
    objects = GameInstanceObjectRelationshipManager()
    
    class Meta:
        unique_together = ('game_instance','subject_game_instance_object','relationship','object_game_instance_object',)

    def __unicode__(self):
        return u'%s' % self.id


# Action Models
class ActionManager(models.Manager):
    def create_action(self, turn, initiator, action, parameters=None, affected=None):
        action = self.create(turn=turn, initiator=initiator, action=action, parameters=parameters, affected=affected)
        return action


class Action(models.Model):
    turn = models.IntegerField()
    initiator = models.ForeignKey(GameInstanceObject, related_name='initiated_actions')
    action = models.ForeignKey(ArchAction, related_name='actions')
    parameters = models.CharField(max_length=255, blank=True, null=True)
    affected = models.ForeignKey(GameInstanceObject, related_name='affected_by_actions', blank=True, null=True)

    objects = ActionManager()

    def __unicode__(self):
        return u'Action id: %s' % self.id


class ActionPermissionManager(models.Manager):
    def create_action_permission(self, action_permission_set, permitted_initiator, action, permitted_affected):
        action_permission = self.create(action_permission_set=action_permission_set, permitted_initiator=permitted_initiator, action=action, permitted_affected=permitted_affected)
        return action_permission
    

class ActionPermission(models.Model):
    action_permission_set = models.ForeignKey(ActionPermissionSet, related_name='action_permissions')
    permitted_initiator = models.ForeignKey(ArchGameObject, related_name='permitted_initiator_actions')
    action = models.ForeignKey(ArchAction)
    permitted_affected = models.ForeignKey(ArchGameObject, related_name='permitted_affected')
    
    objects = ActionPermissionManager()
    
    class Meta:
        unique_together = ('action_permission_set','permitted_initiator','action','permitted_affected',)
    
    def __unicode__(self):
        return u'Permission id: %s' % self.id


class ExoAction(models.Model):
    exo_action_set = models.ForeignKey(ExoActionSet, related_name='exo_actions')
    exo_action = models.ForeignKey(ArchAction, related_name='exo_actions')
    parameters = models.CharField(max_length=255, blank=True, null=True)
    affected = models.ForeignKey(GameObject, related_name='exo_actions', blank=True, null=True)
    turn = models.IntegerField()
    
    class Meta:
        unique_together = ('exo_action_set','exo_action','parameters','affected','turn',)
    
    def __unicode__(self):
        return u'Exogenous action id: %s' % self.id
    
    def create_instance_exo_action(self, game_instance):
        initiator = game_instance.game_instance_objects.all().get(
                game_object__game_object__arch_game_object='nature',
                )
        affected = None
        try:
            affected = game_instance.game_instance_objects.all().get(
                    game_object=self.affected
                    )
        except:
            pass
        instance_exo_action = Action.objects.create_action(turn=self.turn, initiator=initiator, action=self.exo_action, parameters=self.parameters, affected=affected)
        return instance_exo_action