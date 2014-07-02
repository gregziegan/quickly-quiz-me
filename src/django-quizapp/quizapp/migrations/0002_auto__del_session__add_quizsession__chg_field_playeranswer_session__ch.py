# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Session'
        db.delete_table(u'quizapp_session')

        # Adding model 'QuizSession'
        db.create_table(u'quizapp_quizsession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.QuizUser'])),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('ended_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.Quiz'])),
        ))
        db.send_create_signal(u'quizapp', ['QuizSession'])


        # Changing field 'PlayerAnswer.session'
        db.alter_column(u'quizapp_playeranswer', 'session_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.QuizSession']))

        # Changing field 'Question.session'
        db.alter_column(u'quizapp_question', 'session_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.QuizSession']))

    def backwards(self, orm):
        # Adding model 'Session'
        db.create_table(u'quizapp_session', (
            ('ended_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.QuizUser'])),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.Quiz'])),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'quizapp', ['Session'])

        # Deleting model 'QuizSession'
        db.delete_table(u'quizapp_quizsession')


        # Changing field 'PlayerAnswer.session'
        db.alter_column(u'quizapp_playeranswer', 'session_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.Session']))

        # Changing field 'Question.session'
        db.alter_column(u'quizapp_question', 'session_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.Session']))

    models = {
        u'quizapp.course': {
            'Meta': {'object_name': 'Course'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'quizapp.playeranswer': {
            'Meta': {'object_name': 'PlayerAnswer'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizapp.QuizUser']"}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizapp.Question']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizapp.QuizSession']"})
        },
        u'quizapp.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ordinal': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizapp.QuizSession']"})
        },
        u'quizapp.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'answer_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizapp.Course']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'quizapp.quizsession': {
            'Meta': {'object_name': 'QuizSession'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizapp.QuizUser']"}),
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizapp.Quiz']"}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'quizapp.quizuser': {
            'Meta': {'object_name': 'QuizUser'},
            'case_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['quizapp']