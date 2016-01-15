from django.shortcuts import render_to_response
from django.views.generic import View
from django.db import connection


class HomeController(View):
    def get(self, request, *args, **kwargs):
        tables = connection.introspection.table_names()
        tables = [table  for table in tables if not table.startswith('django')]
        return render_to_response('frontend/tables.html', {'tables':tables})

class TableDataController(View):
    
    def get(self, request, *args, **kwargs):
        table = kwargs['table']
        module = __import__('dbinterface')
        class_ = getattr(module.models, table.title())
        instance = class_()
        contents = instance._default_manager.raw('select * from '+ table)        
        return render_to_response('frontend/table_contents.html', {'contents': contents })


class TableDataController1(View):
    
    def get(self, request, *args, **kwargs):
        table = kwargs['table']
        module = __import__('dbinterface')
        class_ = getattr(module.models, table.title())
        instance = class_()
        contents = instance._default_manager.raw('select * from '+ table)        
        return render_to_response('frontend/table_contents.html', {'contents': contents })