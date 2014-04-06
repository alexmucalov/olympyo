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
	game = models.ForeignKey(Game)
	type = models.CharField(max_length=30)
	label = models.CharField(max_length=255)
	default_value = models.CharField(max_length=255)
	
	def __unicode__(self):
		return u'%s: id=%s' % (self.type, self.id)

	def get_instance_copy(self, instance):
		return GameInstanceObject.objects.create(instance=instance, game_object=self, value=self.default_value)


class WaitRoom(models.Model):
	game = models.ForeignKey(Game)
	user = models.ForeignKey(User)
	
	def __unicode__(self):
		return u'%s: id=%s' % (self.game, self.user)


# Game Instance Models
# Created only when enough users are in waitroom! Doesn't exist beforehand
class GameInstance(models.Model):
	game = models.ForeignKey(Game)
	users = models.ManyToManyField(User)
	
	def __unicode__(self):
		return u'%s: id=%s' % (self.game, self.id)


class GameInstanceObject(models.Model):
	instance = models.ForeignKey(GameInstance)
	game_object = models.ForeignKey(GameObject)
	value = models.CharField(max_length=255)

	def __unicode__(self):
		return u'Game instance: %s, id=%s' % (self.instance, self.id)
		

class Action(models.Model):
    instance = models.ForeignKey(GameInstance)
    turn = models.IntegerField()
    initiator = models.ForeignKey(GameObject)
    function = models.CharField(max_length=30)
    parameters = models.CharField(max_length=30)
    affected = models.CharField(max_length=30)

    def __unicode__(self):
		return u'%s' % self.id

