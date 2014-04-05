from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
	id = models.AutoField(primary_key=True)
	rules = models.CharField(max_length=30)
	
	def __unicode__(self):
		return u"%s" % self.id


# Table of users who are in a waiting room, identified by username; launched = playing a game right now
class ActiveUser(models.Model):
	user = models.ForeignKey(User, null=True)
	game = models.ForeignKey(Game)
	launched = models.BooleanField()
  
	def __unicode__(self):
		return u"%s" % self.user


class GameParameter(models.Model):
	game = models.ForeignKey(Game)
	parameter = models.CharField(max_length=30)
	value = models.CharField(max_length=30)


class Instance(models.Model):
	user = models.ForeignKey(User, null=True)
	type = models.CharField(max_length=30)
	
	def __unicode__(self):
		return u"%s" % self.id


class Action(models.Model):
    game = models.ForeignKey(Game)
    turn = models.IntegerField()
    initiator = models.ForeignKey(Instance)
    function = models.CharField(max_length=30)
    parameters = models.CharField(max_length=30)
    affected = models.CharField(max_length=30)

    #def __unicode__(self):
		#return u"%s" % self.id


class InitState(models.Model):
    game = models.ForeignKey(Game)
    instance = models.ForeignKey(Instance)
    attribute = models.CharField(max_length=30)
    value = models.CharField(max_length=30)
    
    #Assign primary keys here? Or let django create auto-increment field?
	
	
class TempState(models.Model):
    game = models.ForeignKey(Game)
    instance = models.ForeignKey(Instance)
    attribute = models.CharField(max_length=30)
    value = models.CharField(max_length=30)
    
    #Assign primary keys here?
    

class WorkingState(models.Model):
    game = models.ForeignKey(Game)
    instance = models.ForeignKey(Instance)
    attribute = models.CharField(max_length=30)
    value = models.CharField(max_length=30)
    
    #Assign primary keys here?

