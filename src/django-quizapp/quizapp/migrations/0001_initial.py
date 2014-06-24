# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Course'
        db.create_table(u'quizapp_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'quizapp', ['Course'])

        # Adding model 'Quiz'
        db.create_table(u'quizapp_quiz', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.Course'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('answer_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'quizapp', ['Quiz'])

        # Adding model 'QuizUser'
        db.create_table(u'quizapp_quizuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('case_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255, db_index=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'quizapp', ['QuizUser'])

        # Adding model 'Session'
        db.create_table(u'quizapp_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.QuizUser'])),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('ended_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.Quiz'])),
        ))
        db.send_create_signal(u'quizapp', ['Session'])

        # Adding model 'Question'
        db.create_table(u'quizapp_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('ordinal', self.gf('django.db.models.fields.IntegerField')()),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.Session'])),
            ('answer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'quizapp', ['Question'])

        # Adding model 'PlayerAnswer'
        db.create_table(u'quizapp_playeranswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.Session'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.QuizUser'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.Question'])),
        ))
        db.send_create_signal(u'quizapp', ['PlayerAnswer'])


    def backwards(self, orm):
        # Deleting model 'Course'
        db.delete_table(u'quizapp_course')

        # Deleting model 'Quiz'
        db.delete_table(u'quizapp_quiz')

        # Deleting model 'QuizUser'
        db.delete_table(u'quizapp_quizuser')

        # Deleting model 'Session'
        db.delete_table(u'quizapp_session')

        # Deleting model 'Question'
        db.delete_table(u'quizapp_question')

        # Deleting model 'PlayerAnswer'
        db.delete_table(u'quizapp_playeranswer')


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
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizapp.Session']"})
        },
        u'quizapp.question': {
            'Meta': {'object_name': 'Question'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ordinal': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizapp.Session']"})
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
        u'quizapp.quizuser': {
            'Meta': {'object_name': 'QuizUser'},
            'case_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'quizapp.session': {
            'Meta': {'object_name': 'Session'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizapp.QuizUser']"}),
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizapp.Quiz']"}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['quizapp']