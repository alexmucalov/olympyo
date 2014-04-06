from django.db import models
from django.contrib.auth.models import User

# Game Template Models
class Game(models.Model):
    name = models.CharField(max_length=30)
    rules = models.CharField(max_length=30)
	
    def __unicode__(self):
        return u'%s' % self.name
	
    def add_user_to_waitroom(self, user):
        pass
		
    def create_instance(self, users):
        instance = GameInstance(game=self, users=users)
        for game_object in self.game_objects.all():
            game_object.get_instance_copy(instance)
        return instance


class GameObject(models.Model):
    game = models.ManyToManyField(Game, related_name='game_objects')
    type = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s: id=%s' % (self.type, self.id)

    def get_instance_copy(self, instance):
        return GameInstanceObject.objects.create(instance=instance, game_object=self, value=self.default_value)


class GameObjectProperty(models.Model):
    game_object = models.ForeignKey(GameObject)
    property = models.CharField(max_length=30)
    init_value = models.CharField(max_length=30)


class WaitRoom(models.Model):
    game = models.ForeignKey(Game, related_name='waitrooms')
    user = models.ForeignKey(User, related_name='waitrooms')
	
    def __unicode__(self):
        return u'%s: id=%s' % (self.game, self.user)


# Game Instance Models
class GameInstance(models.Model):
    game = models.ForeignKey(Game, related_name='game_instances')
    users = models.ManyToManyField(User, related_name='game_instances')
	
    def __unicode__(self):
        return u'%s: id=%s' % (self.game, self.id)


class GameInstanceObject(models.Model):
    instance = models.ForeignKey(GameInstance, related_name='game_instance_objects')
    game_object = models.ForeignKey(GameObject, related_name='game_instance_objects')

    def __unicode__(self):
        return u'Game instance: %s, id=%s' % (self.instance, self.id)
		

class GameInstanceObjectProperty(models.Model):
    game_instance_object = models.ForeignKey(GameInstanceObject)
    game_object_property = models.ForeignKey(GameObjectProperty)
    value = models.CharField(max_length=30)


# Action Models
class Action(models.Model):
    instance = models.ForeignKey(GameInstance, related_name='actions')
    turn = models.IntegerField()
    initiator = models.ForeignKey(GameObject, related_name='actions')
    function = models.CharField(max_length=30)
    parameters = models.CharField(max_length=30)
    affected = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % self.id

"""
remember model managers (see Jared's e-mail for example usage)
remember to use instance methods
"""