# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MetaFields',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('verbose_name', models.CharField(max_length=100)),
                ('other_verbose_names', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='MetaTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('verbose_name', models.CharField(max_length=100)),
                ('other_verbose_names', models.CharField(max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='metafields',
            name='table',
            field=models.ForeignKey(to='query_preprocessing.MetaTable'),
        ),
    ]
