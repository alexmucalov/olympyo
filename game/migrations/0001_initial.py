# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LoggedUser'
        db.create_table(u'game_loggeduser', (
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
        ))
        db.send_create_signal(u'game', ['LoggedUser'])

        # Adding model 'Game'
        db.create_table(u'game_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rules', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['Game'])

        # Adding model 'GameParameter'
        db.create_table(u'game_gameparameter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game'])),
            ('parameter', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['GameParameter'])

        # Adding model 'Instance'
        db.create_table(u'game_instance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['Instance'])

        # Adding model 'Action'
        db.create_table(u'game_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game'])),
            ('turn', self.gf('django.db.models.fields.IntegerField')()),
            ('initiator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Instance'])),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('parameters', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('affected', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['Action'])

        # Adding model 'InitState'
        db.create_table(u'game_initstate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game'])),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Instance'])),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['InitState'])

        # Adding model 'TempState'
        db.create_table(u'game_tempstate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game'])),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Instance'])),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['TempState'])

        # Adding model 'WorkingState'
        db.create_table(u'game_workingstate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Game'])),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['game.Instance'])),
            ('attribute', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'game', ['WorkingState'])


    def backwards(self, orm):
        # Deleting model 'LoggedUser'
        db.delete_table(u'game_loggeduser')

        # Deleting model 'Game'
        db.delete_table(u'game_game')

        # Deleting model 'GameParameter'
        db.delete_table(u'game_gameparameter')

        # Deleting model 'Instance'
        db.delete_table(u'game_instance')

        # Deleting model 'Action'
        db.delete_table(u'game_action')

        # Deleting model 'InitState'
        db.delete_table(u'game_initstate')

        # Deleting model 'TempState'
        db.delete_table(u'game_tempstate')

        # Deleting model 'WorkingState'
        db.delete_table(u'game_workingstate')


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
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'game.loggeduser': {
            'Meta': {'object_name': 'LoggedUser'},
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'})
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