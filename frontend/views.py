from django.shortcuts import render_to_response
from django.views.generic import View
from django.db import connection
from query_preprocessing.type_classifier import predictType
from query_preprocessing.process_query import getNounPhrases,\
    labelTransformedQuery, splitNLQuery, identifyAttribute, \
    identifyConstraints


class HomeController(View):
    def get(self, request, *args, **kwargs):
        tables = connection.introspection.table_names()
        tables = [table  for table in tables if not table.startswith('django')]
        dbtable = request.GET.get('dbtable', None)
        query = request.GET.get('query', None)
        if dbtable and query:
            queryType = predictType(query)
            splittedQuery = splitNLQuery(query)
            # queryLabeled = labelTransformedQuery(splittedQuery, dbtable) 
            # split the selector using , or and and pass all of them separately into identify Attribute.
            _ , selectors = identifyAttribute(splittedQuery[0], dbtable)
            constraints = identifyConstraints(splittedQuery[1], dbtable)
            return render_to_response('frontend/home.html',
                                      {'tables': tables,
                                       'query': query,
                                       'queryType': queryType,
                                       # 'queryIntermediate': queryTrans,
                                       'selectors': selectors,
                                       'constraints': constraints,
                                       'query': query,
                                       })
        return render_to_response('frontend/home.html', {'tables':tables})

class TableDataController1(View):
    
    def get(self, request, *args, **kwargs):
        table = kwargs['table']
        module = __import__('dbinterface')
        class_ = getattr(module.models, table.title())
        instance = class_()
        contents = instance._default_manager.raw('select * from '+ table)        
        return render_to_response('frontend/home.html', {'contents': contents })