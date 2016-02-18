# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Countrynew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('code', models.CharField(db_column='Code', max_length=3)),
                ('name', models.CharField(db_column='Name', max_length=52)),
                ('continent', models.CharField(db_column='Continent', max_length=13)),
                ('region', models.CharField(db_column='Region', max_length=26)),
                ('surfacearea', models.FloatField(db_column='SurfaceArea')),
                ('yearofindependence', models.SmallIntegerField(blank=True, db_column='YearOfIndependence', null=True)),
                ('population', models.IntegerField(db_column='Population')),
                ('lifeexpectancy', models.FloatField(blank=True, db_column='LifeExpectancy', null=True)),
                ('gnp', models.FloatField(blank=True, db_column='GNP', null=True)),
                ('gnpold', models.FloatField(blank=True, db_column='GNPOld', null=True)),
                ('localname', models.CharField(db_column='LocalName', max_length=45)),
                ('governmentform', models.CharField(db_column='GovernmentForm', max_length=45)),
                ('headofstate', models.CharField(blank=True, db_column='HeadOfState', null=True, max_length=60)),
                ('capitalcity', models.CharField(db_column='CapitalCity', max_length=35)),
                ('capitalcitypopulation', models.IntegerField(db_column='CapitalCityPopulation')),
                ('officiallanguage', models.CharField(db_column='OfficialLanguage', max_length=30)),
            ],
            options={
                'managed': False,
                'db_table': 'countryNew',
            },
        ),
    ]
