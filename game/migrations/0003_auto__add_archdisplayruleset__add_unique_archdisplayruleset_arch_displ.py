# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArchDisplayRuleset'
        db.create_table(u'game_archdisplayruleset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('arch_display_ruleset', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'game', ['ArchDisplayRuleset'])

        # Adding unique constraint on 'ArchDisplayRuleset', fields ['arch_display_ruleset']
        db.create_unique(u'game_archdisplayruleset', ['arch_display_ruleset'])

        # Adding unique constraint on 'GameRule', fields ['game_rules']
        db.create_unique(u'game_gamerule', ['game_rules'])

        # Adding unique constraint on 'ArchRelationship', fields ['arch_relationship']
        db.create_unique(u'game_archrelationship', ['arch_relationship'])

        # Adding unique constraint on 'ArchGameObject', fields ['arch_game_object']
        db.create_unique(u'game_archgameobject', ['arch_game_object'])

        # Adding unique constraint on 'ArchLayoutType', fields ['arch_layout']
        db.create_unique(u'game_archlayouttype', ['arch_layout'])

        # Adding unique constraint on 'ArchAttribute', fields ['arch_attribute']
        db.create_unique(u'game_archattribute', ['arch_attribute'])

        # Adding unique constraint on 'GameObjectSet', fields ['game_object_set']
        db.create_unique(u'game_gameobjectset', ['game_object_set'])

        # Adding field 'Game.display_ruleset'
        db.add_column(u'game_game', 'display_ruleset',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, related_name='games', to=orm['game.ArchDisplayRuleset']),
                      keep_default=False)

        # Adding unique constraint on 'ArchAttributeSet', fields ['attribute_set']
        db.create_unique(u'game_archattributeset', ['attribute_set'])

        # Adding unique constraint on 'ArchAction', fields ['arch_action']
        db.create_unique(u'game_archaction', ['arch_action'])


    def backwards(self, orm):
        # Removing unique constraint on 'ArchAction', fields ['arch_action']
        db.delete_unique(u'game_archaction', ['arch_action'])

        # Removing unique constraint on 'ArchAttributeSet', fields ['attribute_set']
        db.delete_unique(u'game_archattributeset', ['attribute_set'])

        # Removing unique constraint on 'GameObjectSet', fields ['game_object_set']
        db.delete_unique(u'game_gameobjectset', ['game_object_set'])

        # Removing unique constraint on 'ArchAttribute', fields ['arch_attribute']
        db.delete_unique(u'game_archattribute', ['arch_attribute'])

        # Removing unique constraint on 'ArchLayoutType', fields ['arch_layout']
        db.delete_unique(u'game_archlayouttype', ['arch_layout'])

        # Removing unique constraint on 'ArchGameObject', fields ['arch_game_object']
        db.delete_unique(u'game_archgameobject', ['arch_game_object'])

        # Removing unique constraint on 'ArchRelationship', fields ['arch_relationship']
        db.delete_unique(u'game_archrelationship', ['arch_relationship'])

        # Removing unique constraint on 'GameRule', fields ['game_rules']
        db.delete_unique(u'game_gamerule', ['game_rules'])

        # Removing unique constraint on 'ArchDisplayRuleset', fields ['arch_display_ruleset']
        db.delete_unique(u'game_archdisplayruleset', ['arch_display_ruleset'])

        # Deleting model 'ArchDisplayRuleset'
        db.delete_table(u'game_archdisplayruleset')

        # Deleting field 'Game.display_ruleset'
        db.delete_column(u'game_game', 'display_ruleset_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'game.action': {
            'Meta': {'object_name': 'Action'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': u"orm['game.ArchAction']"}),
            'affected': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'affected_by_actions'", 'null': 'True', 'to': u"orm['game.GameInstanceObject']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'initiated_actions'", 'to': u"orm['game.GameInstanceObject']"}),
            'parameters': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'turn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'game.archaction': {
            'Meta': {'unique_together': "(('arch_action',),)", 'object_name': 'ArchAction'},
            'arch_action': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.archattribute': {
            'Meta': {'unique_together': "(('arch_attribute',),)", 'object_name': 'ArchAttribute'},
            'arch_attribute': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.archattributeset': {
            'Meta': {'unique_together': "(('attribute_set',),)", 'object_name': 'ArchAttributeSet'},
            'attribute_set': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.archdisplayruleset': {
            'Meta': {'unique_together': "(('arch_display_ruleset',),)", 'object_name': 'ArchDisplayRuleset'},
            'arch_display_ruleset': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.archgameobject': {
            'Meta': {'unique_together': "(('arch_game_object',),)", 'object_name': 'ArchGameObject'},
            'arch_game_object': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layout_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.ArchLayoutType']"})
        },
        u'game.archgameobjectattributevalue': {
            'Meta': {'unique_together': "(('arch_game_object', 'attribute'),)", 'object_name': 'ArchGameObjectAttributeValue'},
            'arch_game_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.ArchGameObject']"}),
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.ArchAttribute']"}),
            'default_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.archlayouttype': {
            'Meta': {'unique_together': "(('arch_layout',),)", 'object_name': 'ArchLayoutType'},
            'arch_layout': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.archrelationship': {
            'Meta': {'unique_together': "(('arch_relationship',),)", 'object_name': 'ArchRelationship'},
            'arch_relationship': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.game': {
            'Meta': {'unique_together': "(('game_object_set', 'game_object_relationship_set', 'game_rules'), ('name',))", 'object_name': 'Game'},
            'display_ruleset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games'", 'to': u"orm['game.ArchDisplayRuleset']"}),
            'game_object_relationship_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games'", 'to': u"orm['game.GameObjectRelationshipSet']"}),
            'game_object_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games'", 'to': u"orm['game.GameObjectSet']"}),
            'game_rules': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'games'", 'to': u"orm['game.GameRule']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'turns': ('django.db.models.fields.IntegerField', [], {})
        },
        u'game.gameinstance': {
            'Meta': {'object_name': 'GameInstance'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'turn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'game.gameinstanceobject': {
            'Meta': {'unique_together': "(('game_instance', 'game_object'),)", 'object_name': 'GameInstanceObject'},
            'game_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_instance_objects'", 'to': u"orm['game.GameInstance']"}),
            'game_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_instance_objects'", 'to': u"orm['game.GameObject']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'game_instance_objects'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'game.gameinstanceobjectattributevalue': {
            'Meta': {'unique_together': "(('game_instance_object', 'attribute'),)", 'object_name': 'GameInstanceObjectAttributeValue'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.ArchAttribute']"}),
            'game_instance_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attribute_values'", 'to': u"orm['game.GameInstanceObject']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'game.gameinstanceobjectrelationship': {
            'Meta': {'unique_together': "(('game_instance', 'subject_game_instance_object', 'relationship', 'object_game_instance_object'),)", 'object_name': 'GameInstanceObjectRelationship'},
            'game_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationships'", 'to': u"orm['game.GameInstance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_game_instance_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationship_objects'", 'to': u"orm['game.GameInstanceObject']"}),
            'relationship': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instance_relationships'", 'to': u"orm['game.ArchRelationship']"}),
            'subject_game_instance_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationship_subjects'", 'to': u"orm['game.GameInstanceObject']"})
        },
        u'game.gameobject': {
            'Meta': {'object_name': 'GameObject'},
            'attribute_set': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'game_objects'", 'null': 'True', 'to': u"orm['game.ArchAttributeSet']"}),
            'game_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_objects'", 'to': u"orm['game.ArchGameObject']"}),
            'game_object_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_objects'", 'to': u"orm['game.GameObjectSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.gameobjectattributevalue': {
            'Meta': {'unique_together': "(('attribute_set', 'attribute'),)", 'object_name': 'GameObjectAttributeValue'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.ArchAttribute']"}),
            'attribute_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attribute_values'", 'to': u"orm['game.ArchAttributeSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'game.gameobjectrelationship': {
            'Meta': {'unique_together': "(('relationship_set', 'subject_game_object', 'relationship', 'object_game_object'),)", 'object_name': 'GameObjectRelationship'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_game_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationship_objects'", 'to': u"orm['game.GameObject']"}),
            'relationship': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationships'", 'to': u"orm['game.ArchRelationship']"}),
            'relationship_set': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationships'", 'to': u"orm['game.GameObjectRelationshipSet']"}),
            'subject_game_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationship_subjects'", 'to': u"orm['game.GameObject']"})
        },
        u'game.gameobjectrelationshipset': {
            'Meta': {'object_name': 'GameObjectRelationshipSet'},
            'game_object_relationship_set': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.gameobjectset': {
            'Meta': {'unique_together': "(('game_object_set',),)", 'object_name': 'GameObjectSet'},
            'game_object_set': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.gamerule': {
            'Meta': {'unique_together': "(('game_rules',),)", 'object_name': 'GameRule'},
            'game_rules': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.waitroom': {
            'Meta': {'object_name': 'Waitroom'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'waitroom'", 'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'waitroom'", 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['game']