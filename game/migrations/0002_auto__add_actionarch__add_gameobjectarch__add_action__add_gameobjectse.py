# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ActionArch'
        db.create_table(u'game_actionarch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action_arch', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['ActionArch'])

        # Adding model 'GameObjectArch'
        db.create_table(u'game_gameobjectarch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_object_arch', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['GameObjectArch'])

        # Adding model 'Action'
        db.create_table(u'game_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('turn', self.gf('django.db.models.fields.IntegerField')()),
            ('initiator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='action_initiators', to=orm['game.GameObjectInstance'])),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actions', to=orm['game.ActionArch'])),
            ('parameters', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('affected', self.gf('django.db.models.fields.related.ForeignKey')(related_name='affected_by_actions', to=orm['game.GameObjectInstance'])),
        ))
        db.send_create_signal(u'game', ['Action'])

        # Adding model 'GameObjectSet'
        db.create_table(u'game_gameobjectset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_object_sets', to=orm['game.Game'])),
            ('game_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_object_sets', to=orm['game.GameObjectArch'])),
            ('no_of_objects', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'game', ['GameObjectSet'])

        # Adding model 'GameObjectInstanceAttribute'
        db.create_table(u'game_gameobjectinstanceattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_object_instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_object_instances', to=orm['game.GameObjectInstance'])),
            ('attribute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.GameObjectArchAttribute'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'game', ['GameObjectInstanceAttribute'])

        # Adding model 'Game'
        db.create_table(u'game_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('rules', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['Game'])

        # Adding model 'GameObjectArchAttribute'
        db.create_table(u'game_gameobjectarchattribute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game_object_arch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.GameObjectArch'])),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('default_value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'game', ['GameObjectArchAttribute'])

        # Adding model 'GameObjectInstance'
        db.create_table(u'game_gameobjectinstance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='game_object_instances', to=orm['game.Game'])),
            ('game_object_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.GameObjectSet'])),
        ))
        db.send_create_signal(u'game', ['GameObjectInstance'])

        # Adding M2M table for field users on 'GameObjectInstance'
        m2m_table_name = db.shorten_name(u'game_gameobjectinstance_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gameobjectinstance', models.ForeignKey(orm[u'game.gameobjectinstance'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['gameobjectinstance_id', 'user_id'])

        # Adding model 'WaitRoomUser'
        db.create_table(u'game_waitroomuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='waitroom_users', to=orm['game.Game'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='waitroom_users', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'game', ['WaitRoomUser'])


    def backwards(self, orm):
        # Deleting model 'ActionArch'
        db.delete_table(u'game_actionarch')

        # Deleting model 'GameObjectArch'
        db.delete_table(u'game_gameobjectarch')

        # Deleting model 'Action'
        db.delete_table(u'game_action')

        # Deleting model 'GameObjectSet'
        db.delete_table(u'game_gameobjectset')

        # Deleting model 'GameObjectInstanceAttribute'
        db.delete_table(u'game_gameobjectinstanceattribute')

        # Deleting model 'Game'
        db.delete_table(u'game_game')

        # Deleting model 'GameObjectArchAttribute'
        db.delete_table(u'game_gameobjectarchattribute')

        # Deleting model 'GameObjectInstance'
        db.delete_table(u'game_gameobjectinstance')

        # Removing M2M table for field users on 'GameObjectInstance'
        db.delete_table(db.shorten_name(u'game_gameobjectinstance_users'))

        # Deleting model 'WaitRoomUser'
        db.delete_table(u'game_waitroomuser')


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
            'action': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': u"orm['game.ActionArch']"}),
            'affected': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'affected_by_actions'", 'to': u"orm['game.GameObjectInstance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'action_initiators'", 'to': u"orm['game.GameObjectInstance']"}),
            'parameters': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'turn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'game.actionarch': {
            'Meta': {'object_name': 'ActionArch'},
            'action_arch': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rules': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'game.gameobjectarch': {
            'Meta': {'object_name': 'GameObjectArch'},
            'game_object_arch': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.gameobjectarchattribute': {
            'Meta': {'object_name': 'GameObjectArchAttribute'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'default_value': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'game_object_arch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.GameObjectArch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'game.gameobjectinstance': {
            'Meta': {'object_name': 'GameObjectInstance'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_object_instances'", 'to': u"orm['game.Game']"}),
            'game_object_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.GameObjectSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'game_object_instances'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'game.gameobjectinstanceattribute': {
            'Meta': {'object_name': 'GameObjectInstanceAttribute'},
            'attribute': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.GameObjectArchAttribute']"}),
            'game_object_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_object_instances'", 'to': u"orm['game.GameObjectInstance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'game.gameobjectset': {
            'Meta': {'object_name': 'GameObjectSet'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_object_sets'", 'to': u"orm['game.Game']"}),
            'game_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'game_object_sets'", 'to': u"orm['game.GameObjectArch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_of_objects': ('django.db.models.fields.IntegerField', [], {})
        },
        u'game.waitroomuser': {
            'Meta': {'object_name': 'WaitRoomUser'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'waitroom_users'", 'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'waitroom_users'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['game']