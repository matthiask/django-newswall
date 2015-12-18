# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newswall', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=128)),
                ('value', models.TextField(null=True, blank=True)),
                ('story', models.ForeignKey(to='newswall.Story')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='extradata',
            unique_together=set([('story', 'key')]),
        ),
    ]
