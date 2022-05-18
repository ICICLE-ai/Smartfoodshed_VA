from neo4j import GraphDatabase, basic_auth

class Neo4jSession: 
    def __init__(self, url, user, password):
        self.driver = GraphDatabase.driver(url, auth=(user, password))

    def close(self, ):
        self.driver.close()

    def update_graph(self, URL, format="tuttle"): 
        

    def query(self, ): 
        pass

    