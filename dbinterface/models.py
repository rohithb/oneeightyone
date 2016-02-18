from __future__ import unicode_literals

from django.db import models


class Countrynew(models.Model):
    code = models.CharField(db_column='Code', verbose_name='Code', max_length=3)  # Field name made lowercase.
    name = models.CharField(db_column='Name',verbose_name='Name', max_length=52)  # Field name made lowercase.
    continent = models.CharField(db_column='Continent',verbose_name='Continent', max_length=13)  # Field name made lowercase.
    region = models.CharField(db_column='Region',verbose_name='Region', max_length=26)  # Field name made lowercase.
    surfacearea = models.FloatField(db_column='SurfaceArea', verbose_name='Surface Area')  # Field name made lowercase.
    yearofindependence = models.SmallIntegerField(db_column='YearOfIndependence',verbose_name='Year of Independence', blank=True, null=True)  # Field name made lowercase.
    population = models.IntegerField(db_column='Population', verbose_name='Population')  # Field name made lowercase.
    lifeexpectancy = models.FloatField(db_column='LifeExpectancy', verbose_name='Life Expectancy', blank=True, null=True)  # Field name made lowercase.
    gnp = models.FloatField(db_column='GNP', verbose_name='GNP', blank=True, null=True)  # Field name made lowercase.
    gnpold = models.FloatField(db_column='GNPOld', verbose_name='Old GNP', blank=True, null=True)  # Field name made lowercase.
    localname = models.CharField(db_column='LocalName', verbose_name='Local Name', max_length=45)  # Field name made lowercase.
    governmentform = models.CharField(db_column='GovernmentForm', verbose_name='Government Form', max_length=45)  # Field name made lowercase.
    headofstate = models.CharField(db_column='HeadOfState', verbose_name='Head of State', max_length=60, blank=True, null=True)  # Field name made lowercase.
    capitalcity = models.CharField(db_column='CapitalCity', verbose_name='Capital City', max_length=35)  # Field name made lowercase.
    capitalcitypopulation = models.IntegerField(db_column='CapitalCityPopulation', verbose_name='Capital City Population')  # Field name made lowercase.
    officiallanguage = models.CharField(db_column='OfficialLanguage', verbose_name='Official Language', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'countryNew'
        verbose_name ='Countries'
