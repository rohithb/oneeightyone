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
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import RegexpParser


def splitNLQuery(query):
    '''
        Need to find out a mechanism to automatically split selector and filter part
        from the query.
        Possibly write a grammer to do so.
    '''
    return query.split("|")

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

def  identifyAttribute(selectorPart, dbtable):
    '''
        To identify a single attribute from the selectorPart
    '''
    metaTable = MetaTable.objects.get(name=dbtable)
    tableAltNames = metaTable.other_verbose_names.split(',')
    tableAltNames.append(metaTable.verbose_name)
    attribute = ''
    queryTrans = getNounPhrases(selectorPart)
    matchedTerm = ''
    for term in queryTrans:
        term = term.lower()
        if term in typeDeterminers:
            continue
        elif term in tableAltNames:
            attribute= "*"
        else:
            fields = MetaFields.objects.filter(name=term, table=metaTable)
            if fields:
                attribute = fields[0].name
            else:
                fields = MetaFields.objects.filter(verbose_name=term, table=metaTable)
                if fields:
                    attribute = fields[0].name
                else:
                    fields = MetaFields.objects.filter(other_verbose_names__contains=term, table=metaTable)
                    if fields:
                        attribute = fields[0].name
        if attribute:
            matchedTerm = term
            break
    if attribute:
        return matchedTerm, attribute
    else:
        attribute = resolveAttrNameUsingKB(selectorPart)
        return matchedTerm, attribute
    
def labelTransformedQuery(query, queryTrans, dbtable):
    '''
        currently not using 
    '''
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

def tag(x):
    return pos_tag(word_tokenize(x))

def findRelationshipStr(phrase):
    adjectives = "JJ JJR JJS".split()
    prepositions = ["IN"]
    phrase = tag(phrase)
    for i in range(len(phrase) - 1):
        if (phrase[i][1] in prepositions) & (phrase[i+1][1] in ["CD"]):
            return [phrase[i][0]]
    return None

    
def findRelationshipUsingGrammer(phrase):
    phrase = tag(phrase)
    grammer ='REL: {<RB><RBR><IN>|' \
                 '<RB><JJ|JJR|JJS><IN>|' \
                 '<JJ|JJR|JJS><IN>|' \
                 '<JJ|JJR|JJS>}'
    parseTree = RegexpParser(grammer).parse(phrase)
    for i in parseTree.subtrees(filter=lambda x: x.label() == 'REL'):
        return ' '.join([ k[0] for k in list(i)])

    
    
def identifyConstraints(constraintsPart, dbtable):
    '''
        OR has less precedence than that of AND.
        Returns a list, relation between each element in the list will be OR
        o/p should look like
        [
            {'AND': [
                        {'attribute': ...,
                         'relatoion': ...,
                         'value': ...
                        },
                        {'attribute': ...,
                         'relatoion': ...,
                         'value': ...
                        }
                    ]
            },
            {'attribute': ...,
             'relatoion': ...,
             'value': ...
            }
        ]
    
    '''
    constraints = []
    if not constraintsPart:
        return []
    constraintsPart = constraintsPart.lower()
    orSplit = constraintsPart.split(' or ')
    for orPart in orSplit:
        andSplit = re.split(' and |,', orPart)
        if len(andSplit) > 1:
            # means and inside or 
            andTemp = []
            for part in andSplit:
                temp = {} 
                matchedTerm, temp['attribute'] = identifyAttribute(part, dbtable)
                # identify relationship
                part = part.replace(matchedTerm, '')
                temp['relation'] = findRelationshipUsingGrammer(part)
                if not temp['relation']:
                    temp['relation'] = findRelationshipStr(part)
                # identify value
                andTemp.append(temp)
            constraints.append({'AND': andTemp})
        else:
            temp = {}
            part = andSplit[0]
            matchedTerm, temp['attribute'] = identifyAttribute(part , dbtable)
            # identify relationship
            part = part.replace(matchedTerm, '')
            temp['relation'] = findRelationshipUsingGrammer(part)
            if not temp['relation']:
                    temp['relation'] = findRelationshipStr(part)
            # identify value
            constraints.append(temp)
    return constraints     
    
