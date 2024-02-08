from neo4j import GraphDatabase
import uuid
import dotenv
import os

dotenv.load_dotenv()

class Neo4jConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri,
                                                 auth=(self.__user,
                                                       self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.__driver.session(
                database=db) if db is not None else self.__driver.session()
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response

    def add_definition(self, worker_id, word, definition, domain):
        # worker_exists_query = "OPTIONAL MATCH (w:Worker {{id: {}}}) RETURN COUNT(w) <> 0".format(worker_id)
        # create_worker_query = "CREATE (worker:Worker {{id: {}, task:'definition', domain:'{}'}})".format(worker_id, domain)
        # if not self.query(worker_exists_query):
        #     self.query(create_worker_query)
        # word_exists_query = "OPTIONAL MATCH (w:Word {{content: '{}'}}) RETURN COUNT(w) IS NOT NULL".format(word)
        # create_word_query = "CREATE (word:Word {{content: '{}'}})".format(word)
        # if not self.query(word_exists_query):
        #     self.query(create_word_query)
        add_query = """
            MERGE (worker:Worker {{id: '{}', task:'definition', domain:'{}'}}) 
            MERGE (word:Word {{content: '{}'}}) 
            CREATE (definition:Definition {{content: '{}'}}) 
            CREATE (worker)-[:HAS_OUTPUT {{id: '{}', status: 'pending'}}]->(definition) 
            CREATE (worker)-[:HAS_INPUT]->(word) 
            CREATE (word)-[:HAS_DEFINITION]->(definition)
            """.format(
            worker_id,
            domain,
            word,
            definition,
            uuid.uuid1().hex,
        )
        self.query(add_query)

    def add_word(self, worker_id, word, domain, task):
        add_query = """
            MERGE (worker:Worker {{id: '{}', task:'{}', domain:'{}'}}) 
            MERGE (word:Word {{content: '{}'}})
            CREATE (worker)-[:HAS_OUTPUT {{id: '{}', status: 'pending'}}]->(word) 
            """.format(
            worker_id,
            task,
            domain,
            word,
            uuid.uuid1().hex,
        )
        self.query(add_query)

    def get_definitions(self, worker_id):
        get_definitions_query = f"""
            MATCH (w:Worker {{id: '{worker_id}'}})-[r:HAS_OUTPUT]->(d:Definition) 
            MATCH (w)-[:HAS_INPUT]->(word:Word) 
            RETURN DISTINCT w.id AS worker, word.content AS word, d.content AS definition, r.status AS status, r.id as rid
        """
        # get_definitions_query = f"MATCH (word:Word)<-[:HAS_INPUT]-(w:Worker {{id: '{worker_id}'}})-[r:HAS_OUTPUT]->(d:Definition) RETURN w.id AS worker, word.content AS word, d.content AS definition, r.status AS status, r.id as rid"
        results = self.query(get_definitions_query)
        if not results:
            return [], self.completion_rate([])
        output = [{
            "word": row['word'],
            "definition": row['definition'],
            "status": row['status'],
            "id_relation": row['rid'],
        } for row in results]
        return output, self.completion_rate(output)
    
    def get_words(self, worker_id):
        get_definitions_query = f"""
            MATCH (w:Worker {{id: '{worker_id}'}})-[r:HAS_OUTPUT]->(word:Word) 
            RETURN DISTINCT w.id AS worker, word.content AS word, r.status AS status, r.id as rid
        """
        # get_definitions_query = f"MATCH (word:Word)<-[:HAS_INPUT]-(w:Worker {{id: '{worker_id}'}})-[r:HAS_OUTPUT]->(d:Definition) RETURN w.id AS worker, word.content AS word, d.content AS definition, r.status AS status, r.id as rid"
        results = self.query(get_definitions_query)
        if not results:
            return [], self.completion_rate([])
        output = [{
            "word": row['word'],
            "status": row['status'],
            "id_relation": row['rid'],
        } for row in results]
        return output, self.completion_rate(output)

    def change_has_output_status(self, has_output_id, new_status):
        change_query = f"MATCH ()-[r:HAS_OUTPUT {{id: '{has_output_id}'}}]->() SET r.status='{new_status}' RETURN r"
        try:
            self.query(change_query)
            return True
        except:
            return False

    def completion_rate(self, data):
        if len(data) == 0:
            return 0
        return (1 - sum([d['status'] == 'pending'
                         for d in data]) / len(data)) * 100


def get_neo4j_connection():
    return Neo4jConnection(uri=os.getenv('NEO4J_URI'),
                           user=os.getenv('NEO4J_USER'),
                           pwd=os.getenv('NEO4J_URI'))
