from data_prep.open_nlp import OpenNLP
from query_preprocessing.helper import typeDeterminers
from nltk.corpus import stopwords
import re
from py2neo import Graph, Node, Relationship
from query_preprocessing.models import MetaTable, MetaFields
import httplib2 as http
import json
from urllib.parse import urlparse
import sys


def getNounPhrases(query):
    posTagger = OpenNLP("/home/rohith/nitk/apache-opennlp-1.6.0", "POSTagger", "en-pos-maxent.bin")
    chunker = OpenNLP("/home/rohith/nitk/apache-opennlp-1.6.0", "ChunkerME", "en-chunker.bin")
    pos = posTagger.parse(query)
    chunks = chunker.parse(pos)
    chunks = chunks.decode()
    queryInter = []
    temp = re.finditer(r"\[NP (\w+\s?[$&+,:;=?@#|'<>.^*()%!-]*)+\]",chunks)
    for item in temp:
        item = item.group().replace('[NP','').replace(']','')
        item = re.sub(r"_(\w)+", '', item).strip()
        queryInter.append(item)
    return queryInter


def labelTransformedQuery(query, queryTrans, dbtable):
    query_processed = {}
    metaTable = MetaTable.objects.get(name=dbtable)
    tableAltNames = metaTable.other_verbose_names.split(',')
    tableAltNames.append(metaTable.verbose_name)
    query_processed['attribute'] = []
    for term in queryTrans:
        term = term.lower()
        if term in typeDeterminers:
            query_processed['typeDetr'] = term
        elif term in tableAltNames:
            query_processed['dbTable'] = {'table_name': metaTable.name,
                                          'query_term': term }
        else:
            # try name
            fields = MetaFields.objects.filter(name=term, table=metaTable)
            if fields:
                query_processed['attribute'].append({'attrName': fields[0].name,
                                                     'query_term': term})
            else:
                fields = MetaFields.objects.filter(verbose_name=term, table=metaTable)
                if fields:
                    query_processed['attribute'].append({'attrName': fields[0].name,
                                                     'query_term': term})
                else:
                    fields = MetaFields.objects.filter(other_verbose_names__contains=term, table=metaTable)
                    if fields:
                        query_processed['attribute'].append({'attrName': fields[0].name,
                                                     'query_term': term})
                    else:
                        query_processed['constraints'] = term
    
    if not query_processed['attribute']:
        attrName = resolveAttrNameUsingKB(query)
        query_processed['attribute'].append({'attrName': attrName})
    return query_processed


def resolveAttrNameUsingKB(query):
    g = Graph()
    large_weight = 0
    large_wt_node = None
    for node in g.find('ROOT'):
        wt = shortestPathWeight(query, node)
        # print(node.properties['phrase']+ ' : '+ str(wt), file=sys.stderr)
        if  wt > large_weight:
            large_wt_node = node
            large_weight = wt
    if large_wt_node is None:
        return ''
    return large_wt_node.properties['phrase']
        
    
    
    

def shortestPathWeight(query, rootNode):
    stop = stopwords.words('english')
    query = query.split()
    g = Graph()
    weight = 0
    for term in query:
        pathSet = set()
        if term not in stop:
            result = g.cypher.execute("MATCH (n:NP) where str(n.phrase) =~ '(?i).*"+term+".*' return n")
            if result:
                for item in result:
                    uri = item.n.graph.uri + item.n.ref + '/path'
                    headers = {
                                    'Accept': 'application/json',
                                    'Content-Type': 'application/json; charset=UTF-8'
                                }
                    target = urlparse(uri.string)
                    method = 'POST'
                    body = {
                                "to": str(rootNode.graph.uri+rootNode.ref),
                                "max_depth": 20,
                                "relationships" : {
                                    "type" : "DEPENDS"
                                  },
                                  "algorithm" : "shortestPath"
                            }
                    body = json.dumps(body)
                    h = http.Http()
                    response, content = h.request(target.geturl(), method, body, headers)
                    try:
                        data = json.loads(content.decode())
                        relationships = data['relationships']
                        for rel in relationships:
                            relId = rel[rel.rfind('/')+1:]
                            rel = g.relationship(relId)
                            pathSet.add(rel.properties['path_id'])
                        weight = weight + harmonicProduct(len(pathSet))
                    except:
                        pass
    return weight

def harmonicProduct(n):
    if n == 0:
        return 0
    pro = float(1)
    for i in range(1, n+1):
        pro = pro * (1.0/i)
    return pro
                            
    