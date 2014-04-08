from django.db import models
from django.contrib.auth.models import User



# Archetype Models
class ActionArch(models.Model):
    action_arch = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % (self.action_arch)


class GameObjectArch(models.Model):
    game_object_arch = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % (self.game_object_arch)


class GameObjectArchAttribute(models.Model):
    game_object_arch = models.ForeignKey(GameObjectArch)
    attribute = models.CharField(max_length=255)
    default_value = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % (self.game_object_arch)

    #def get_instance_copy(self, instance):
    #    return GameInstanceObject.objects.create(instance=instance, game_object=self, value=self.default_value)



# Game Template Models
class Game(models.Model):
    name = models.CharField(max_length=255)
    rules = models.CharField(max_length=30)
    
    def __unicode__(self):
        return u'%s' % self.name


class GameObjectSet(models.Model):
    game = models.ForeignKey(Game, related_name='game_object_sets')
    game_object = models.ForeignKey(GameObjectArch, related_name='game_object_sets')
    no_of_objects = models.IntegerField()

    def __unicode__(self):
        return u'%s: %s' % (self.game_object, self.game)
	
    def add_user_to_waitroom(self, user):
        pass
		
    #def create_instance(self, users):
    #    instance = GameInstance(game=self, users=users)
    #    for game_object in self.game_objects.all():
    #        game_object.get_instance_copy(instance)
    #    return instance


class WaitRoomUser(models.Model):
    game = models.ForeignKey(Game, related_name='waitroom_users')
    user = models.ForeignKey(User, related_name='waitroom_users')
	
    def __unicode__(self):
        return u'%s: id=%s' % (self.game, self.user)



# Game Instance Models
class GameObjectInstance(models.Model):
    game_object_instance = models.ForeignKey(GameObjectSet, related_name='game_object_instances')
    users = models.ManyToManyField(User, related_name='game_object_instances', blank=True, null=True)
	
    def __unicode__(self):
        return u'%s: instance id=%s' % (self.game_object_instance, self.id)


class GameObjectInstanceAttribute(models.Model):
    game_object_instance = models.ForeignKey(GameObjectInstance, related_name='game_object_instances')
    attribute = models.ForeignKey(GameObjectArchAttribute)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % (self.game_object)



# Action Models
class Action(models.Model):
    turn = models.IntegerField()
    initiator = models.ForeignKey(GameObjectInstance, related_name='action_initiators')
    action = models.ForeignKey(ActionArch, related_name='actions')
    parameters = models.CharField(max_length=30)
    affected = models.ForeignKey(GameObjectInstance, related_name='affected_by_actions')

    def __unicode__(self):
        return u'Action id: %s' % self.id




"""
remember model managers (see Jared's e-mail for example usage)
remember to use instance methods
"""