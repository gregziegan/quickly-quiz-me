# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PlayerAnswer.content'
        db.alter_column(u'quizapp_playeranswer', 'content', self.gf('django.db.models.fields.TextField')(null=True))
        # Deleting field 'Question.session'
        db.delete_column(u'quizapp_question', 'session_id')

        # Adding field 'Question.quiz'
        db.add_column(u'quizapp_question', 'quiz',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['quizapp.Quiz']),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'PlayerAnswer.content'
        raise RuntimeError("Cannot reverse this migration. 'PlayerAnswer.content' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'PlayerAnswer.content'
        db.alter_column(u'quizapp_playeranswer', 'content', self.gf('django.db.models.fields.TextField')())

        # User chose to not deal with backwards NULL issues for 'Question.session'
        raise RuntimeError("Cannot reverse this migration. 'Question.session' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Question.session'
        db.add_column(u'quizapp_question', 'session',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['quizapp.QuizSession']),
                      keep_default=False)

        # Deleting field 'Question.quiz'
        db.delete_column(u'quizapp_question', 'quiz_id')


    models = {
        u'quizapp.course': {
            'Meta': {'object_name': 'Course'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'quizapp.playeranswer': {
            'Meta': {'object_name': 'PlayerAnswer'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quizapp.Quiz']"})
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
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'permission_level': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['quizapp']