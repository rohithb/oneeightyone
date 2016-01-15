from pymongo import MongoClient
from data_prep.config import mongo, neo4j
from py2neo import Graph, Node, Relationship, authenticate


class DBCrawl:

    def __init__(self):
        self.db = mongo['db_name']
        self.host = mongo['host']
        self.port = mongo['port']
        self.client = MongoClient(self.host, self.port)
        authenticate(neo4j['host'] + ':' + neo4j['port'],
                     neo4j['username'], neo4j['password'])
        self.graph = Graph()

    def _getCollections(self):
        collections = self.client.db.getCollectionNames()
        for collection in collections:
            return collections

    def _migrate_data(self, collection, neo4j_label):
        '''
            :param collection: The collection object that need to be _migrate_data
            :param neo4j_label: The label to be used in Neo4j for this collection
        '''
        for item in collection.find({}):
            try:
                item.pop('_id', None)
                node = Node(neo4j_label, **item)
                self.graph.create(node)
            except Exception as e:
                print(str(e))

    def migrate_relations_acquisition_company(self):
        for acq in self.graph.find("Acquisition"):
            comp = self.graph.find_one(
                "Company", "name", acq.properties['acquirer_name'])
            ac_to_comp = Relationship(acq, "details", comp)
            self.graph.create(ac_to_comp)

    def migrate_relations_company_acquisition(self):
        for comp in self.graph.find("Company"):
            acq = self.graph.find_one(
                "Acquisition", "company_name", comp.properties['name'])
            comp_to_ac = Relationship(comp, "acquisition", acq)
            self.graph.create(comp_to_ac)

    def migrate_all_collections(self):
        collections = self._getCollections()
        for collection in collections:
            self._migrate_data(collection, collection.name)
        self.migrate_relations_company_acquisition()
        self.migrate_relations_acquisition_company()
