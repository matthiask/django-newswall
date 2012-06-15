# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Story.title'
        db.alter_column('newswall_story', 'title', self.gf('django.db.models.fields.CharField')(max_length=1000))

        # Changing field 'Story.image_url'
        db.alter_column('newswall_story', 'image_url', self.gf('django.db.models.fields.CharField')(max_length=1000))

    def backwards(self, orm):
        
        # Changing field 'Story.title'
        db.alter_column('newswall_story', 'title', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Story.image_url'
        db.alter_column('newswall_story', 'image_url', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        'newswall.source': {
            'Meta': {'ordering': "['ordering', 'name']", 'object_name': 'Source'},
            'data': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'newswall.story': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Story'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'object_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': "orm['newswall.Source']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['newswall']
