from neo4j import GraphDatabase
import uuid

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
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
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
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
        add_query ="MERGE (worker:Worker {{id: {}, task:'definition', domain:'{}'}}) MERGE (word:Word {{content: '{}'}}) CREATE (definition:Definition {{content: '{}'}}) CREATE (worker)-[:HAS_OUTPUT {{id: '{}', status: 'pending'}}]->(definition) CREATE (worker)-[:HAS_INPUT]->(word) CREATE (word)-[:HAS_DEFINITION]->(definition)".format(worker_id, domain, word, definition, worker_id, uuid.uuid4(), word)
        self.query(add_query)
    
    def get_definitions(self, worker_id):
        get_definitions_query = f"MATCH (word:Word)<-[:HAS_INPUT]-(w:Worker {{id: {worker_id}}})-[r:HAS_OUTPUT]->(d:Definition) RETURN w.id AS worker, word.content AS word, d.content AS definition, r.status AS status"
        results = self.query(get_definitions_query)
        output = [{"word": row['word'], "definition": row['definition'], "status": row['status']} for row in results]
        return output