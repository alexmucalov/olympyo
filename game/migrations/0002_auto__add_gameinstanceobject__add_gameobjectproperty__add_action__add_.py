# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GameInstanceObject'
        db.create_table(u'game_gameinstanceobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_instance_objects', to=orm['game.GameInstance'])),
            ('game_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_instance_objects', to=orm['game.GameObject'])),
        ))
        db.send_create_signal(u'game', ['GameInstanceObject'])

        # Adding model 'GameObjectProperty'
        db.create_table(u'game_gameobjectproperty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.GameObject'])),
            ('property', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('init_value', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['GameObjectProperty'])

        # Adding model 'Action'
        db.create_table(u'game_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['game.GameInstance'])),
            ('turn', self.gf('django.db.models.fields.IntegerField')()),
            ('initiator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['game.GameObject'])),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('parameters', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('affected', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['Action'])

        # Adding model 'GameInstanceObjectProperty'
        db.create_table(u'game_gameinstanceobjectproperty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_instance_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.GameInstanceObject'])),
            ('game_object_property', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.GameObjectProperty'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['GameInstanceObjectProperty'])

        # Adding model 'GameObject'
        db.create_table(u'game_gameobject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['GameObject'])

        # Adding M2M table for field game on 'GameObject'
        m2m_table_name = db.shorten_name(u'game_gameobject_game')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gameobject', models.ForeignKey(orm[u'game.gameobject'], null=False)),
            ('game', models.ForeignKey(orm[u'game.game'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gameobject_id', 'game_id'])

        # Adding model 'GameInstance'
        db.create_table(u'game_gameinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_instances', to=orm['game.Game'])),
        ))
        db.send_create_signal(u'game', ['GameInstance'])

        # Adding M2M table for field users on 'GameInstance'
        m2m_table_name = db.shorten_name(u'game_gameinstance_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gameinstance', models.ForeignKey(orm[u'game.gameinstance'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gameinstance_id', 'user_id'])

        # Adding model 'Game'
        db.create_table(u'game_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('rules', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['Game'])

        # Adding model 'WaitRoom'
        db.create_table(u'game_waitroom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='waitrooms', to=orm['game.Game'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='waitrooms', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'game', ['WaitRoom'])


    def backwards(self, orm):
        # Deleting model 'GameInstanceObject'
        db.delete_table(u'game_gameinstanceobject')

        # Deleting model 'GameObjectProperty'
        db.delete_table(u'game_gameobjectproperty')

        # Deleting model 'Action'
        db.delete_table(u'game_action')

        # Deleting model 'GameInstanceObjectProperty'
        db.delete_table(u'game_gameinstanceobjectproperty')

        # Deleting model 'GameObject'
        db.delete_table(u'game_gameobject')

        # Removing M2M table for field game on 'GameObject'
        db.delete_table(db.shorten_name(u'game_gameobject_game'))

        # Deleting model 'GameInstance'
        db.delete_table(u'game_gameinstance')

        # Removing M2M table for field users on 'GameInstance'
        db.delete_table(db.shorten_name(u'game_gameinstance_users'))

        # Deleting model 'Game'
        db.delete_table(u'game_game')

        # Deleting model 'WaitRoom'
        db.delete_table(u'game_waitroom')


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
            'affected': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': u"orm['game.GameObject']"}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': u"orm['game.GameInstance']"}),
            'parameters': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'turn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'rules': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'game.gameinstance': {
            'Meta': {'object_name': 'GameInstance'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_instances'", 'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'game_instances'", 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'game.gameinstanceobject': {
            'Meta': {'object_name': 'GameInstanceObject'},
            'game_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_instance_objects'", 'to': u"orm['game.GameObject']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_instance_objects'", 'to': u"orm['game.GameInstance']"})
        },
        u'game.gameinstanceobjectproperty': {
            'Meta': {'object_name': 'GameInstanceObjectProperty'},
            'game_instance_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.GameInstanceObject']"}),
            'game_object_property': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.GameObjectProperty']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'game.gameobject': {
            'Meta': {'object_name': 'GameObject'},
            'game': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'game_objects'", 'symmetrical': 'False', 'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'game.gameobjectproperty': {
            'Meta': {'object_name': 'GameObjectProperty'},
            'game_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.GameObject']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'init_value': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'property': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'game.waitroom': {
            'Meta': {'object_name': 'WaitRoom'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'waitrooms'", 'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'waitrooms'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['game']