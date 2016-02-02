from django.http import HttpResponse
from data_prep.preprocessingFuncs import fetchSentsFromPages
from data_prep.depParsingFuncs import parseContents
from py2neo import Graph, Node, Relationship, authenticate
import logging


logger = logging.getLogger(__name__)


def fetchBackgroundInfo(request):

    urlList = ['http://localhost/wiki.html',]
    contents = fetchSentsFromPages(urlList)
#     contents = [''' A sale is the exchange of a commodity or money as the price of a good or a service. Sales is activity related to selling or the amount of sold goods or services in a given time period.
#                 The seller or the provider of the goods or services completes a sale in response to an acquisition, appropriation, requisition or a direct interaction with the buyer at the point of sale. There is a passing of title (property or ownership) of the item, and the settlement of a price, in which agreement is reached on a price for which transfer of ownership of the item will occur. The seller, not the purchaser generally executes the sale and it may be completed prior to the obligation of payment. In the case of indirect interaction, a person who sells goods or service on behalf of the owner is known as salesman or saleswoman.
#                 In common law countries, sales are governed generally by the common law and commercial codes. In the United States, the laws governing sales of goods are somewhat uniform to the extent that most jurisdictions have adopted Article 2 of the Uniform Commercial Code, albeit with some non-uniform variations.
#                 ''']
    logger.info('Contents fetched')
#     tupleList = parseContents(contents)
    authenticate("localhost:7474", "neo4j", "root")
    graph = Graph()
    try:
        graph.schema.create_uniqueness_constraint('subject', 'phrase')
        graph.schema.create_uniqueness_constraint('predicate', 'phrase')
        graph.schema.create_uniqueness_constraint('object', 'phrase')
    except:
        pass
    for tup in parseContents(contents):
        try:
            nodeNp1 = graph.create(Node("subject", phrase=tup[0].lower()))
        except:
            nodeNp1 = graph.find_one("subject", "phrase", tup[0].lower())
            
        try:
            nodeVp = graph.create(Node("predicate", phrase=tup[1].lower()))
        except:
            nodeVp = graph.find_one("predicate", "phrase", tup[1].lower())
        
        try:
            nodeNp2 = graph.create(Node("object", phrase=tup[2].lower()))
        except:
            nodeNp2 = graph.find_one("object", "phrase", tup[2].lower())

        if type(nodeNp1) == tuple:
            nodeNp1 = nodeNp1[0]
        if type(nodeVp) == tuple:
            nodeVp = nodeVp[0]
        if type(nodeNp2) == tuple:
            nodeNp2 = nodeNp2[0]
            
        vpNp1Dep = Relationship(nodeVp, "DEPENDS", nodeNp1, weight=0) # need to change the weight
        vpNp2Dep = Relationship(nodeVp, "DEPENDS", nodeNp2, weight=0)
        graph.create_unique(vpNp1Dep)
        graph.create_unique(vpNp2Dep)
    return HttpResponse("true")
