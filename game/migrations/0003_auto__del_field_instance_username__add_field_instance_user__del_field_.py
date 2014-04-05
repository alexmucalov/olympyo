# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Instance.username'
        db.delete_column(u'game_instance', 'username_id')

        # Adding field 'Instance.user'
        db.add_column(u'game_instance', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True),
                      keep_default=False)

        # Deleting field 'ActiveUser.username'
        db.delete_column(u'game_activeuser', 'username_id')

        # Adding field 'ActiveUser.user'
        db.add_column(u'game_activeuser', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Instance.username'
        raise RuntimeError("Cannot reverse this migration. 'Instance.username' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Instance.username'
        db.add_column(u'game_instance', 'username',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Instance.user'
        db.delete_column(u'game_instance', 'user_id')


        # User chose to not deal with backwards NULL issues for 'ActiveUser.username'
        raise RuntimeError("Cannot reverse this migration. 'ActiveUser.username' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ActiveUser.username'
        db.add_column(u'game_activeuser', 'username',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'ActiveUser.user'
        db.delete_column(u'game_activeuser', 'user_id')


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
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initiator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Instance']"}),
            'parameters': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'turn': ('django.db.models.fields.IntegerField', [], {})
        },
        u'game.activeuser': {
            'Meta': {'object_name': 'ActiveUser'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'launched': ('django.db.models.fields.BooleanField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'game.game': {
            'Meta': {'object_name': 'Game'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rules': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'game.gameparameter': {
            'Meta': {'object_name': 'GameParameter'},
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'game.initstate': {
            'Meta': {'object_name': 'InitState'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Instance']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'game.instance': {
            'Meta': {'object_name': 'Instance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'game.tempstate': {
            'Meta': {'object_name': 'TempState'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Instance']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'game.workingstate': {
            'Meta': {'object_name': 'WorkingState'},
            'attribute': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Game']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['game.Instance']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['game']