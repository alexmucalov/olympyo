from django.db import models
from django.contrib.auth.models import User


# Game Rules Models
class GameRule(models.Model):
    game_rules = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % (self.game_rules)



# Archetype Models
class ArchAction(models.Model):
    arch_action = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % (self.arch_action)


class ArchAttribute(models.Model):
    arch_attribute = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % (self.arch_attribute)


class ArchGameObject(models.Model):
    arch_game_object = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % (self.arch_game_object)


class ArchGameObjectAttributeValue(models.Model):
    arch_game_object = models.ForeignKey(ArchGameObject)
    attribute = models.ForeignKey(ArchAttribute)
    default_value = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s: %s' % (self.arch_game_object, self.attribute)

    #def get_instance_copy(self, instance):
    #    return GameInstanceObject.objects.create(instance=instance, game_object=self, value=self.default_value)



# Game Template Models
class GameObjectSet(models.Model):
    game_object_set = models.CharField(max_length=255)
    
    def __unicode__(self):
        return u'%s' % self.game_object_set


# Good! Ideally, though, could only choose sets that apply to the same game object types
# as GameObjectTypeValuesDefined


class GameObject(models.Model):
    # May want to make game_object_set a ManyToManyField
    game_object_set = models.ForeignKey(GameObjectSet, related_name='game_objects')
    game_object = models.ForeignKey(ArchGameObject, related_name='game_objects')
    attribute_set = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % (self.game_object)
	
    def add_user_to_waitroom(self, user):
        pass
		
    #def create_instance(self, users):
    #    instance = GameInstance(game=self, users=users)
    #    for game_object in self.game_objects.all():
    #        game_object.get_instance_copy(instance)
    #    return instance


class AttributeValue(models.Model):
    attribute_set = models.ForeignKey(GameObject) # Ideally would be defined and available for a given game_object_type, and no other
    attribute = models.ForeignKey(ArchAttribute)
    value = models.CharField(max_length = 255)

    def __unicode__(self):
        return u'%s: %s - %s' % (self.attribute_set, self.attribute, self.value)


class Game(models.Model):
    game_object_set = models.ForeignKey(GameObjectSet, related_name='games')
    game_rules = models.ForeignKey(GameRule, related_name='games')
    # Game is the same if rules and object_set are the same - can define more precisely like this? With 'unique' or something like this?

    def __unicode__(self):
        return u'%s: id=%s' % (self.game, self.user)


class WaitRoomUser(models.Model):
    game = models.ForeignKey(Game, related_name='waitroom_users')
    user = models.ManyToManyField(User, related_name='waitroom_users')
	
    def __unicode__(self):
        return u'%s: id=%s' % (self.game, self.user)



# Game Instance Models
class GameInstance(models.Model):
    game = models.ForeignKey(Game)
    
    def __unicode__(self):
        return u'%s: id=%s' % (self.game, self.id)


class GameInstanceObject(models.Model):
    game_instance = models.ForeignKey(GameInstance, related_name='game_instance_objects')
    game_object = models.ForeignKey(GameObject, related_name='game_instance_objects')
    users = models.ManyToManyField(User, related_name='game_instance_objects', blank=True, null=True)
	
    def __unicode__(self):
        return u'%s: instance id=%s' % (self.game_object_instance, self.id)


class GameInstanceObjectAttributeValue(models.Model):
    game_instance_object = models.ForeignKey(GameInstanceObject, related_name='game_instance_object_attribute_values')
    attribute = models.ForeignKey(ArchAttribute)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % (self.attribute)



# Action Models
class Action(models.Model):
    turn = models.IntegerField()
    initiator = models.ForeignKey(GameInstanceObject, related_name='action_initiators')
    action = models.ForeignKey(ArchAction, related_name='actions')
    parameters = models.CharField(max_length=30)
    affected = models.ForeignKey(GameInstanceObject, related_name='affected_by_actions')

    def __unicode__(self):
        return u'Action id: %s' % self.id




"""
remember model managers (see Jared's e-mail for example usage)
remember to use instance methods
"""