from neo4j import GraphDatabase, basic_auth

class Neo4jSession: 
    def __init__(self, url, user, password):
        self.driver = GraphDatabase.driver(url, auth=(user, password))

    def close(self, ):
        self.driver.close()


    @staticmethod
    def dataReturnFromPathRecord(records): 
    nodes_list = []
    relationships = []
    for record in records: 
        value = record.values()[0]
        start_node_raw = value.start_node
        start_node = {
            "type": "node", 
            "id": start_node_raw.id,
            "labels": list(start_node_raw.labels),
            "properties": {item[0]: item[1] for item in start_node_raw.items()}
            
        }
        if start_node['properties'].get("name"): 
            start_node['properties']["name"] = str(start_node['properties']["name"])
        end_node_raw = value.end_node
        
        end_node = {
            "type": "node", 
            "id": end_node_raw.id,
            "labels": list(end_node_raw.labels),
            "properties": {item[0]: item[1] for item in end_node_raw.items()}
            
        }
        
        if end_node['properties'].get("name"): 
            end_node['properties']["name"] = str(end_node['properties']["name"])
        relationships_raw = value.relationships[0]
        
        relationship = {
            "id": relationships_raw.id, 
            "startNode": start_node_raw.id, 
            "endNode": end_node_raw.id,
            "label": relationships_raw.type,
            "properties": {item[0]: item[1] for item in relationships_raw.items()}
        }
        
        nodes_list.append(start_node)
        nodes_list.append(end_node)
        
        relationships.append(relationship)
    return {"results": [{
            "columns": [],
            "data": [
        {
            "graph": {
                "nodes": nodes_list,
                "relationships": relationships
            }
        }
    ]}]}