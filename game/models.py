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

    #def get_instance_copy(self, instance):
    #    return GameInstanceObject.objects.create(instance=instance, game_object=self, value=self.default_value)


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
        return u'%s' % self.game_object_relationships


class GameObject(models.Model):
    game_object_set = models.ForeignKey(GameObjectSet, related_name='game_objects')
    game_object = models.ForeignKey(ArchGameObject, related_name='game_objects')
    attribute_set = models.ForeignKey(ArchAttributeSet, related_name='game_objects', blank=True, null=True)
    # Ideally, game_object would determine attribute_sets available...

    def __unicode__(self):
        return u'%s: id=%s' % (self.game_object, self.id)
	
    def add_user_to_waitroom(self, user):
        pass
		
    #def create_instance(self, users):
    #    instance = GameInstance(game=self, users=users)
    #    for game_object in self.game_objects.all():
    #        game_object.get_instance_copy(instance)
    #    return instance


class GameObjectRelationship(models.Model):
    relationship_set = models.ForeignKey(GameObjectRelationshipSet, related_name='relationships')
    subject_game_object = models.ForeignKey(GameObject, related_name='game_object_relationship_subjects')
    relationship = models.ForeignKey(ArchRelationship, related_name='relationships')
    object_game_object = models.ForeignKey(GameObject, related_name='game_object_relationship_objects')

    class Meta:
        unique_together = ('relationship_set','subject_game_object','relationship','object_game_object',)

    def __unicode__(self):
        return u'id=%s' % self.id


class AttributeValue(models.Model):
    attribute_set = models.ForeignKey(ArchAttributeSet)
    attribute = models.ForeignKey(ArchAttribute)
    value = models.CharField(max_length = 255)
    # Ideally would be defined and available for a given game_object_type, and no other
    
    class Meta:
        unique_together = ('attribute_set','attribute')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.attribute_set, self.attribute, self.value)


class Game(models.Model):
    game_object_set = models.ForeignKey(GameObjectSet, related_name='games')
    game_object_relationship_set = models.ForeignKey(GameObjectRelationshipSet, related_name='games')
    game_rules = models.ForeignKey(GameRule, related_name='games')

    class Meta:
        unique_together = ('game_object_set','game_object_relationship_set','game_rules')

    def __unicode__(self):
        return u'%s: id=%s' % (self.game_object_set, self.id)


class Waitroom(models.Model):
    game = models.ForeignKey(Game, related_name='waitroom')
    user = models.ManyToManyField(User, related_name='waitroom')
	
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
	
    class Meta:
	    unique_together = ('game_instance','game_object')

    def __unicode__(self):
        return u'%s: instance id=%s' % (self.game_object, self.id)


class GameInstanceObjectAttributeValue(models.Model):
    game_instance_object = models.ForeignKey(GameInstanceObject, related_name='game_instance_object_attribute_values')
    attribute = models.ForeignKey(ArchAttribute)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('game_instance_object','attribute')

    def __unicode__(self):
        return u'%s' % (self.attribute)


class GameInstanceObjectRelationship(models.Model):
    game_instance = models.ForeignKey(GameInstance, related_name='relationships')
    subject_game_instance_object = models.ForeignKey(GameObject, related_name='game_instance_object_relationship_subjects')
    relationship = models.ForeignKey(ArchRelationship, related_name='instance_relationships')
    object_game_instance_object = models.ForeignKey(GameObject, related_name='game_instance_object_relationship_objects')
    
    class Meta:
        unique_together = ('game_instance','subject_game_instance_object','relationship','object_game_instance_object',)

    def __unicode__(self):
        return u'%s' % self.id



# Action Models
class Action(models.Model):
    turn = models.IntegerField()
    initiator = models.ForeignKey(GameInstanceObject, related_name='action_initiators')
    action = models.ForeignKey(ArchAction, related_name='actions')
    parameters = models.CharField(max_length=30)
    affected = models.ForeignKey(GameInstanceObject, related_name='affected_by_actions')

    class Meta:
        unique_together = ('turn','initiator','action','parameters','affected',)

    def __unicode__(self):
        return u'Action id: %s' % self.id




"""
remember model managers (see Jared's e-mail for example usage)
remember to use instance methods
"""