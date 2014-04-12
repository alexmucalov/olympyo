# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GameRule'
        db.create_table(u'game_gamerule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_rules', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['GameRule'])

        # Adding model 'ArchRelationship'
        db.create_table(u'game_archrelationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('arch_relationship', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'game', ['ArchRelationship'])

        # Adding model 'ArchGameObject'
        db.create_table(u'game_archgameobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('arch_game_object', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'game', ['ArchGameObject'])

        # Adding model 'GameInstanceObject'
        db.create_table(u'game_gameinstanceobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_instance_objects', to=orm['game.GameInstance'])),
            ('game_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_instance_objects', to=orm['game.GameObject'])),
        ))
        db.send_create_signal(u'game', ['GameInstanceObject'])

        # Adding M2M table for field users on 'GameInstanceObject'
        m2m_table_name = db.shorten_name(u'game_gameinstanceobject_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gameinstanceobject', models.ForeignKey(orm[u'game.gameinstanceobject'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gameinstanceobject_id', 'user_id'])

        # Adding unique constraint on 'GameInstanceObject', fields ['game_instance', 'game_object']
        db.create_unique(u'game_gameinstanceobject', ['game_instance_id', 'game_object_id'])

        # Adding model 'ArchAttribute'
        db.create_table(u'game_archattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('arch_attribute', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['ArchAttribute'])

        # Adding model 'Action'
        db.create_table(u'game_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('turn', self.gf('django.db.models.fields.IntegerField')()),
            ('initiator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='initiated_actions', to=orm['game.GameInstanceObject'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['game.ArchAction'])),
            ('parameters', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('affected', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='affected_by_actions', null=True, to=orm['game.GameInstanceObject'])),
        ))
        db.send_create_signal(u'game', ['Action'])

        # Adding model 'GameObjectSet'
        db.create_table(u'game_gameobjectset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_object_set', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'game', ['GameObjectSet'])

        # Adding model 'GameInstanceObjectAttributeValue'
        db.create_table(u'game_gameinstanceobjectattributevalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_instance_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='attribute_values', to=orm['game.GameInstanceObject'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.ArchAttribute'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'game', ['GameInstanceObjectAttributeValue'])

        # Adding unique constraint on 'GameInstanceObjectAttributeValue', fields ['game_instance_object', 'attribute']
        db.create_unique(u'game_gameinstanceobjectattributevalue', ['game_instance_object_id', 'attribute_id'])

        # Adding model 'GameObject'
        db.create_table(u'game_gameobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_object_set', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_objects', to=orm['game.GameObjectSet'])),
            ('game_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_objects', to=orm['game.ArchGameObject'])),
            ('attribute_set', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='game_objects', null=True, to=orm['game.ArchAttributeSet'])),
        ))
        db.send_create_signal(u'game', ['GameObject'])

        # Adding model 'Game'
        db.create_table(u'game_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('game_object_set', self.gf('django.db.models.fields.related.ForeignKey')(related_name='games', to=orm['game.GameObjectSet'])),
            ('game_object_relationship_set', self.gf('django.db.models.fields.related.ForeignKey')(related_name='games', to=orm['game.GameObjectRelationshipSet'])),
            ('game_rules', self.gf('django.db.models.fields.related.ForeignKey')(related_name='games', to=orm['game.GameRule'])),
            ('turns', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'game', ['Game'])

        # Adding unique constraint on 'Game', fields ['game_object_set', 'game_object_relationship_set', 'game_rules']
        db.create_unique(u'game_game', ['game_object_set_id', 'game_object_relationship_set_id', 'game_rules_id'])

        # Adding unique constraint on 'Game', fields ['name']
        db.create_unique(u'game_game', ['name'])

        # Adding model 'GameInstance'
        db.create_table(u'game_gameinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game'])),
            ('turn', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'game', ['GameInstance'])

        # Adding model 'Waitroom'
        db.create_table(u'game_waitroom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='waitroom', to=orm['game.Game'])),
        ))
        db.send_create_signal(u'game', ['Waitroom'])

        # Adding M2M table for field user on 'Waitroom'
        m2m_table_name = db.shorten_name(u'game_waitroom_user')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('waitroom', models.ForeignKey(orm[u'game.waitroom'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['waitroom_id', 'user_id'])

        # Adding model 'GameObjectRelationshipSet'
        db.create_table(u'game_gameobjectrelationshipset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_object_relationship_set', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'game', ['GameObjectRelationshipSet'])

        # Adding model 'ArchAttributeSet'
        db.create_table(u'game_archattributeset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attribute_set', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'game', ['ArchAttributeSet'])

        # Adding model 'GameObjectRelationship'
        db.create_table(u'game_gameobjectrelationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('relationship_set', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationships', to=orm['game.GameObjectRelationshipSet'])),
            ('subject_game_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationship_subjects', to=orm['game.GameObject'])),
            ('relationship', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationships', to=orm['game.ArchRelationship'])),
            ('object_game_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationship_objects', to=orm['game.GameObject'])),
        ))
        db.send_create_signal(u'game', ['GameObjectRelationship'])

        # Adding unique constraint on 'GameObjectRelationship', fields ['relationship_set', 'subject_game_object', 'relationship', 'object_game_object']
        db.create_unique(u'game_gameobjectrelationship', ['relationship_set_id', 'subject_game_object_id', 'relationship_id', 'object_game_object_id'])

        # Adding model 'GameInstanceObjectRelationship'
        db.create_table(u'game_gameinstanceobjectrelationship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationships', to=orm['game.GameInstance'])),
            ('subject_game_instance_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationship_subjects', to=orm['game.GameInstanceObject'])),
            ('relationship', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instance_relationships', to=orm['game.ArchRelationship'])),
            ('object_game_instance_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationship_objects', to=orm['game.GameInstanceObject'])),
        ))
        db.send_create_signal(u'game', ['GameInstanceObjectRelationship'])

        # Adding unique constraint on 'GameInstanceObjectRelationship', fields ['game_instance', 'subject_game_instance_object', 'relationship', 'object_game_instance_object']
        db.create_unique(u'game_gameinstanceobjectrelationship', ['game_instance_id', 'subject_game_instance_object_id', 'relationship_id', 'object_game_instance_object_id'])

        # Adding model 'AttributeValue'
        db.create_table(u'game_attributevalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attribute_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.ArchAttributeSet'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.ArchAttribute'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'game', ['AttributeValue'])

        # Adding unique constraint on 'AttributeValue', fields ['attribute_set', 'attribute']
        db.create_unique(u'game_attributevalue', ['attribute_set_id', 'attribute_id'])

        # Adding model 'ArchGameObjectAttributeValue'
        db.create_table(u'game_archgameobjectattributevalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('arch_game_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.ArchGameObject'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.ArchAttribute'])),
            ('default_value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'game', ['ArchGameObjectAttributeValue'])

        # Adding unique constraint on 'ArchGameObjectAttributeValue', fields ['arch_game_object', 'attribute']
        db.create_unique(u'game_archgameobjectattributevalue', ['arch_game_object_id', 'attribute_id'])

        # Adding model 'ArchAction'
        db.create_table(u'game_archaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('arch_action', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['ArchAction'])


    def backwards(self, orm):
        # Removing unique constraint on 'ArchGameObjectAttributeValue', fields ['arch_game_object', 'attribute']
        db.delete_unique(u'game_archgameobjectattributevalue', ['arch_game_object_id', 'attribute_id'])

        # Removing unique constraint on 'AttributeValue', fields ['attribute_set', 'attribute']
        db.delete_unique(u'game_attributevalue', ['attribute_set_id', 'attribute_id'])

        # Removing unique constraint on 'GameInstanceObjectRelationship', fields ['game_instance', 'subject_game_instance_object', 'relationship', 'object_game_instance_object']
        db.delete_unique(u'game_gameinstanceobjectrelationship', ['game_instance_id', 'subject_game_instance_object_id', 'relationship_id', 'object_game_instance_object_id'])

        # Removing unique constraint on 'GameObjectRelationship', fields ['relationship_set', 'subject_game_object', 'relationship', 'object_game_object']
        db.delete_unique(u'game_gameobjectrelationship', ['relationship_set_id', 'subject_game_object_id', 'relationship_id', 'object_game_object_id'])

        # Removing unique constraint on 'Game', fields ['name']
        db.delete_unique(u'game_game', ['name'])

        # Removing unique constraint on 'Game', fields ['game_object_set', 'game_object_relationship_set', 'game_rules']
        db.delete_unique(u'game_game', ['game_object_set_id', 'game_object_relationship_set_id', 'game_rules_id'])

        # Removing unique constraint on 'GameInstanceObjectAttributeValue', fields ['game_instance_object', 'attribute']
        db.delete_unique(u'game_gameinstanceobjectattributevalue', ['game_instance_object_id', 'attribute_id'])

        # Removing unique constraint on 'GameInstanceObject', fields ['game_instance', 'game_object']
        db.delete_unique(u'game_gameinstanceobject', ['game_instance_id', 'game_object_id'])

        # Deleting model 'GameRule'
        db.delete_table(u'game_gamerule')

        # Deleting model 'ArchRelationship'
        db.delete_table(u'game_archrelationship')

        # Deleting model 'ArchGameObject'
        db.delete_table(u'game_archgameobject')

        # Deleting model 'GameInstanceObject'
        db.delete_table(u'game_gameinstanceobject')

        # Removing M2M table for field users on 'GameInstanceObject'
        db.delete_table(db.shorten_name(u'game_gameinstanceobject_users'))

        # Deleting model 'ArchAttribute'
        db.delete_table(u'game_archattribute')

        # Deleting model 'Action'
        db.delete_table(u'game_action')

        # Deleting model 'GameObjectSet'
        db.delete_table(u'game_gameobjectset')

        # Deleting model 'GameInstanceObjectAttributeValue'
        db.delete_table(u'game_gameinstanceobjectattributevalue')

        # Deleting model 'GameObject'
        db.delete_table(u'game_gameobject')

        # Deleting model 'Game'
        db.delete_table(u'game_game')

        # Deleting model 'GameInstance'
        db.delete_table(u'game_gameinstance')

        # Deleting model 'Waitroom'
        db.delete_table(u'game_waitroom')

        # Removing M2M table for field user on 'Waitroom'
        db.delete_table(db.shorten_name(u'game_waitroom_user'))

        # Deleting model 'GameObjectRelationshipSet'
        db.delete_table(u'game_gameobjectrelationshipset')

        # Deleting model 'ArchAttributeSet'
        db.delete_table(u'game_archattributeset')

        # Deleting model 'GameObjectRelationship'
        db.delete_table(u'game_gameobjectrelationship')

        # Deleting model 'GameInstanceObjectRelationship'
        db.delete_table(u'game_gameinstanceobjectrelationship')

        # Deleting model 'AttributeValue'
        db.delete_table(u'game_attributevalue')

        # Deleting model 'ArchGameObjectAttributeValue'
        db.delete_table(u'game_archgameobjectattributevalue')

        # Deleting model 'ArchAction'
        db.delete_table(u'game_archaction')


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
            'parameters': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'turn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'game.archaction': {
            'Meta': {'object_name': 'ArchAction'},
            'arch_action': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.archattribute': {
            'Meta': {'object_name': 'ArchAttribute'},
            'arch_attribute': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.archattributeset': {
            'Meta': {'object_name': 'ArchAttributeSet'},
            'attribute_set': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.archgameobject': {
            'Meta': {'object_name': 'ArchGameObject'},
            'arch_game_object': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.archgameobjectattributevalue': {
            'Meta': {'unique_together': "(('arch_game_object', 'attribute'),)", 'object_name': 'ArchGameObjectAttributeValue'},
            'arch_game_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.ArchGameObject']"}),
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.ArchAttribute']"}),
            'default_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.archrelationship': {
            'Meta': {'object_name': 'ArchRelationship'},
            'arch_relationship': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.attributevalue': {
            'Meta': {'unique_together': "(('attribute_set', 'attribute'),)", 'object_name': 'AttributeValue'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.ArchAttribute']"}),
            'attribute_set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.ArchAttributeSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'game.game': {
            'Meta': {'unique_together': "(('game_object_set', 'game_object_relationship_set', 'game_rules'), ('name',))", 'object_name': 'Game'},
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
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'game_instance_objects'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
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
            'Meta': {'object_name': 'GameObjectSet'},
            'game_object_set': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.gamerule': {
            'Meta': {'object_name': 'GameRule'},
            'game_rules': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.waitroom': {
            'Meta': {'object_name': 'Waitroom'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'waitroom'", 'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'waitroom'", 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['game']