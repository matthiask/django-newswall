# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('data', models.TextField(verbose_name='configuration data', blank=True)),
            ],
            options={
                'ordering': ['ordering', 'name'],
                'verbose_name': 'source',
                'verbose_name_plural': 'sources',
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now, verbose_name='timestamp')),
                ('object_url', models.URLField(unique=True, verbose_name='object URL')),
                ('title', models.CharField(max_length=1000, verbose_name='title')),
                ('author', models.CharField(max_length=100, verbose_name='author', blank=True)),
                ('body', models.TextField(help_text='Content of the story. May contain HTML.', verbose_name='body', blank=True)),
                ('image_url', models.CharField(max_length=1000, verbose_name='image URL', blank=True)),
                ('source', models.ForeignKey(related_name='stories', verbose_name='source', to='newswall.Source')),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': 'story',
                'verbose_name_plural': 'stories',
            },
        ),
    ]
