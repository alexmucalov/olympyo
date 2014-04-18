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


class ArchAttributeSet(models.Model):
    attribute_set = models.CharField(max_length=255)
    #game_object = models.ForeignKey(ArchGameObject)
    # Might need game_object to add extra validation - when adding attribute_set
    # to GameObject, check that game_object fields in both models match

    def __unicode__(self):
        return u'%s' % (self.attribute_set)


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

    def __unicode__(self):
        return u'%s' % self.arch_relationship


# Game Template Models
class GameObjectSet(models.Model):
    game_object_set = models.CharField(max_length=255)
    
    def __unicode__(self):
        return u'%s' % self.game_object_set


class GameObjectRelationshipSet(models.Model):
    game_object_relationship_set = models.CharField(max_length=255)
    #game_object_set = models.ForeignKey(GameObjectSet)
    # Might need game_object_set to add extra validation - when adding game_object_relationship_set
    # to Game, check that game_object_set fields in both models match
        
    def __unicode__(self):
        return u'%s' % self.game_object_relationship_set


class GameObject(models.Model):
    game_object_set = models.ForeignKey(GameObjectSet, related_name='game_objects')
    game_object = models.ForeignKey(ArchGameObject, related_name='game_objects')
    attribute_set = models.ForeignKey(ArchAttributeSet, related_name='game_objects', blank=True, null=True)
    # Ideally, game_object would determine attribute_sets available...

    def __unicode__(self):
        return u'%s: id=%s' % (self.game_object, self.id)

    def create_instance_object(self, game_instance, users=None):
        game_object = self
        instance_object = GameInstanceObject.objects.create_game_instance_object(game_instance=game_instance, game_object=game_object)
        if users:
            instance_object.users.add(users)
        return instance_object


class GameObjectRelationship(models.Model):
    relationship_set = models.ForeignKey(GameObjectRelationshipSet, related_name='relationships')
    subject_game_object = models.ForeignKey(GameObject, related_name='relationship_subjects')
    relationship = models.ForeignKey(ArchRelationship, related_name='relationships')
    object_game_object = models.ForeignKey(GameObject, related_name='relationship_objects')

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


class AttributeValue(models.Model):
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


class Game(models.Model):
    name = models.CharField(max_length=255)
    game_object_set = models.ForeignKey(GameObjectSet, related_name='games')
    game_object_relationship_set = models.ForeignKey(GameObjectRelationshipSet, related_name='games')
    game_rules = models.ForeignKey(GameRule, related_name='games')
    turns = models.IntegerField()

    class Meta:
        unique_together = (('game_object_set','game_object_relationship_set','game_rules',),('name',),)

    def __unicode__(self):
        return u'%s' % (self.name)

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
            game_instance_object = game_object.create_instance_object(game_instance, game_object_user)
            if game_object.attribute_set:
                for attribute_value in game_object.attribute_set.attribute_values.all():
                    game_instance_object_attribute_value = attribute_value.create_instance_attribute_value(game_instance_object)
        for game_object_relationship in self.game_object_relationship_set.relationships.all():
            game_object_relationship.create_instance_object_relationship(game_instance)
        

class Waitroom(models.Model):
    game = models.ForeignKey(Game, related_name='waitroom')
    user = models.ManyToManyField(User, related_name='waitroom')
	#Should be labelled 'users', on a many to many field
	
    def __unicode__(self):
        return u'%s: id=%s' % (self.game, self.user)

    #def add_user(self, request):
        #room = request.room
        #waitroom = Waitroom.objects.get(id=room)
        #waitroom.add(request.user)
        #waitroom_user_count = waitroom.user_set.all().count()
        #game_player_count = waitroom.game.game_object_set.game_objects.all().filter(game_object__arch_game_object='player').count()
        #if waitroom_user_count >= game_player_count:
        #    Send users to /game/, using nodejs or Python Twisted
        #    self.game.create_all_instance_objects(users)


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


class GameInstanceObjectManager(models.Manager):
    def create_game_instance_object(self, game_instance, game_object):
        game_instance_object = self.create(game_instance=game_instance, game_object=game_object)
        return game_instance_object


class GameInstanceObject(models.Model):
    game_instance = models.ForeignKey(GameInstance, related_name='game_instance_objects')
    game_object = models.ForeignKey(GameObject, related_name='game_instance_objects')
    users = models.ManyToManyField(User, related_name='game_instance_objects', blank=True, null=True)
    
    objects = GameInstanceObjectManager()
	
    class Meta:
	    unique_together = ('game_instance','game_object')

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
    parameters = models.CharField(max_length=30, blank=True, null=True)
    affected = models.ForeignKey(GameInstanceObject, related_name='affected_by_actions', blank=True, null=True)

    objects = ActionManager()

    def __unicode__(self):
        return u'Action id: %s' % self.id