from django.db import models


class MetaTable(models.Model):
    name = models.CharField(max_length=100)
    verbose_name = models.CharField(max_length=100)
    other_verbose_names = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name

class MetaFields(models.Model):
    table = models.ForeignKey(MetaTable)
    name = models.CharField(max_length=100)
    verbose_name = models.CharField(max_length=100)
    other_verbose_names = models.CharField(max_length=300)
    
    def __str__(self):
        return self.name