from django.db import models
from django.contrib.auth.models import User


# Table of users who are logged in, identified by username
class LoggedUser(models.Model):
	username = models.CharField(max_length=30, primary_key=True)
  
	def __unicode__(self):
		return self.username


class Game(models.Model):
	rules = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.id


class GameParameter(models.Model):
	game = models.ForeignKey(Game)
	parameter = models.CharField(max_length=30)
	value = models.CharField(max_length=30)


class Instance(models.Model):
	username = models.ForeignKey(User)
	type = models.CharField(max_length=30)
	
	def __unicode__(self):
		return self.id


class Action(models.Model):
    game = models.ForeignKey(Game)
    turn = models.IntegerField()
    initiator = models.ForeignKey(Instance)
    function = models.CharField(max_length=30)
    parameters = models.CharField(max_length=30)
    affected = models.CharField(max_length=30)

    #def __unicode__(self):
		#return self.id


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

