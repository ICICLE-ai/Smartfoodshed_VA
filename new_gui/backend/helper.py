from neo4j import GraphDatabase, basic_auth
import ast
import json
from itertools import combinations,product
from py2neo import Subgraph
import collections
import py2neo


def filterGraph(data, num, sort):
    ## filter nodes 
    nodes = data['results'][0]['data'][0]['graph']['nodes']
    
    #reformat nodes into the dict list 
    reformat_nodes = []
    for node in nodes:
        reformat_nodes.append({
            'id': node['id'],
            'influence_average': node['properties']['influence_average'],
            'influence_sum': node['properties']['influence_sum'],
            'degree': node['properties']['degree'],
            'influence_adj': node['properties']['influence_adj'],
            'betweenness': node['properties']['betweenness'],
            'pagerank': node['properties']['pagerank'],
            'name': node['properties']['name'],
            'community': node['properties']['community']
        })
    new_nodes = sorted(reformat_nodes, key = lambda i: i[sort],reverse=True)[0:num]

    edges = data['results'][0]['data'][0]['graph']['relationships']
    valid_node_ids = [ele['id'] for ele in new_nodes]
    new_edges = []

    for e in edges:
        if e['startNode'] in valid_node_ids and e['endNode'] in valid_node_ids:
            new_edges.append(e)
    
    backformat = []
    for node in new_nodes:
        backformat.append({
            'type':'node',
            'id': node['id'],
            'labels': ['ENTITY'],
            'properties':{
                'influence_average': node['influence_average'],
                'influence_sum': node['influence_sum'],
                'degree': node['degree'],
                'name': node['name'],
                'influence_adj': node['influence_adj'],
                'betweenness': node['betweenness'],
                'id': node['name'],
                'pagerank': node['pagerank'],
                'community': node['community']
            }
        })
   
    output = {
        "results": [{
            "columns":[],
            "data":[{
                "graph":{
                    "nodes": backformat,
                    "relationships":new_edges
                }
            }]
        }],
        "errors":[]
    }
    return output

def preprocess_county_entity(node_list,graph):
    #Add geo_id to all county entities
    #Add node label "County" to all county entities
    set_county_label_cypher = "MATCH (n) WHERE id(n) = {} SET n:County"
    set_geoid_cypher = "MATCH (n) WHERE id(n) = {} SET n.geo_id = '{}'"
    fips = pd.read_csv("county_fips.csv")
    fips = fips.astype({"fips": str})
    fips['fips'] = fips['fips'].apply(lambda x: x.zfill(5))
    fips = fips.append({'fips':'46102', 'name':'Oglala Lakota County','state':'SD'},ignore_index=True)
    for node in node_list:
        node = graph.nodes.get(node_id)
        if node["geo_id"] is None:
            graph.run(set_county_label_cypher.format(node.identity))
            geo_id = fips[fips.name.isin([node["label"]])]['fips'].values[0]
            graph.run(set_geoid_cypher.format(node.identity,geo_id))

def get_county_info(node_list,graph):
    count_type_cypher = "match (n)-[p]-(m) where id(n) = {} and type(p) = \"in_county\" return labels(m) as type, count(m) as amount"
    county_list = []
    for node in node_list:
        cypher_result = graph.run(count_type_cypher.format(node.identity)).data()
        count_details = {r["type"][1]: r["amount"] for r in cypher_result}
        count_total = sum(count_details.values())
        county_id = node["geo_id"]
        county_dict = {"county_id":county_id,"count_total":count_total,"count_details":count_details}
        county_list.append(county_dict)
    return county_list

def write_county_info_to_json(out_file,graph):
    incounty_edges = graph.relationships.match(r_type="in_county").all()
    county_node_id = list(set([i.end_node.identity for i in incounty_edges]))
    node_list = [graph.nodes.get(i) for i in county_node_id]
    # preprocess_county_entity(node_list,graph)
    out_dict = get_county_info(node_list)
    out_file = "map_data.json"
    with open(out_file, 'w') as outfile:
        json.dump(out_dict, outfile)

# Input: a graph object from py2neo,
#           entity_type is a string,
#           limit_number denotes the maximum number of entity instance you want to get
#Output: entity_list, a list of dictionary, includes the table_data
#         table_info, a list of dictionary, includes the table info
def entity_table(graph, entity_type, limit_number=None):
    if not limit_number:
        all_entities = graph.nodes.match(entity_type).all()
    else:
        all_entities = graph.nodes.match(entity_type).limit(limit_number)
    entity_list = []
    # get the table info
    keys = list(all_entities[0].keys())
    values = list(all_entities[0].values())
    table_info = []
    for index, i in enumerate(keys):
        info_dict = {"label": i, "value": i, "type": str(type(values[index]).__name__)}
        table_info.append(info_dict)

    # start to construct the entity list
    for entity in all_entities:
        entity_dict = dict(entity)
        entity_dict.update({"id": entity.identity})
        entity_list.append(entity_dict)
    return entity_list, table_info

# Input:    graph, a graph object from py2neo,
#           relation_type is a string, denotes the relationship type which you want to generate a table
#           entity_identifier, a string, denotes the property name which you want to display in the front end (same as the mapping property)
#           entity_identifier, a string, denotes the property name which you want to display in the front end (same as the mapping property)
#           limit_number, denotes the maximum number of relationship instance you want to get
#Output: relation_list, a list of dictionary, includes the table_data
#         table_info, a list of dictionary, includes the table info
def relation_table(graph, relation_type, entity_identifier, limit_number=None):
    if not limit_number:
        all_relation = graph.relationships.match(r_type=relation_type).all()
    else:
        all_relation = graph.relationships.match(r_type=relation_type).limit(limit_number).all()
    relation_list = []

    # get table info
    keys = list(all_relation[0].keys())
    values = list(all_relation[0].values())
    table_info = []
    for index, i in enumerate(keys):
        info_dict = {"label": i, "value": i, "type": str(type(values[index]).__name__)}
        table_info.append(info_dict)
    # add the starting node and ending node column
    start_node_name = list(all_relation[0].start_node.labels)[0] + "_start"
    end_node_name = list(all_relation[0].end_node.labels)[0] + "_start"
    table_info.append({"label": start_node_name, "value": start_node_name, "type": "str"})
    table_info.append({"label": end_node_name, "value": end_node_name, "type": "str"})

    # start to construct the relation list
    for relation in all_relation:
        start_entity_type = list(relation.start_node.labels)[0] + "_start"
        end_entity_type = list(relation.end_node.labels)[0] + "_end"
        relation_id = relation.identity
        start_id = relation.start_node.identity
        end_id = relation.end_node.identity
        start_node = relation.start_node[entity_identifier]
        end_node = relation.end_node[entity_identifier]
        r_dict = {start_entity_type: start_node, end_entity_type: end_node, "relation_id": relation_id,
                  "start_id": start_id, "end_id": end_id}
        r_dict.update(dict(relation))
        relation_list.append(r_dict)
    return relation_list, table_info

#Input: graph, a graph object from py2neo
#       entity_type_list, a list of entity_type
#       out_file, the path for the out put file
#       limit_number, a number indicating the maximum number of instance we want to put in the table
def write_entities_to_json(graph,entity_type_list,out_file,limit_number=None):
    entity_table_list = []
    for entity in entity_type_list:
        table_data,table_info = entity_table(graph,entity,limit_number)
        entity_dic = {"table_name":entity,"table_data":table_data,"table_info":table_info}
        entity_table_list.append(entity_dic)
    with open(out_file, 'w') as outfile:
        json.dump(entity_table_list, outfile)

#Input: graph, a graph object from py2neo
#       relation_type_list, a list of relationship_type
#       out_file, the path for the out put file
#       entity_identifier, a string, denotes the property name which you want to display in the front end (same as the mapping property)
#       limit_number, a number indicating the maximum number of instance we want to put in the table
def write_relations_to_json(graph,relation_type_list,out_file,entity_identifier,limit_number=None):
    relation_table_list = []
    for relation in relation_type_list:
        table_data,table_info = relation_table(graph,relation,entity_identifier,limit_number)
        relation_dic = {"table_name":relation,"table_data":table_data,"table_info":table_info}
        relation_table_list.append(relation_dic)
    with open(out_file, 'w') as outfile:
        json.dump(relation_table_list, outfile)

#Input: graph, a graph object from py2neo
#       node_id_list, a list of int, each element is an id for a node
#       relation_id_list, a list of int, each element is an id for a relationship
#Ouput: a sugraph object in py2neo
def get_subgraph(graph, node_id_list, relation_id_list):
    node_list = [graph.nodes.get(i) for i in node_id_list]
    all_pairs = [set(comb) for comb in combinations(node_list, 2)]
    subgraph = Subgraph()

    # get all the relationships where the ending node and starting node all belong to the node set and put in the subgraph
    for pair in all_pairs:
        relation = graph.match(pair).first()
        if relation is not None:
            subgraph = subgraph | relation

    # concatenate the subgraph with relationship list
    relation_list = [graph.relationships.get(i) for i in relation_id_list]
    subgraph = subgraph | Subgraph((), relation_list)

    # concatenate the subgraph with node list
    subgraph = subgraph | Subgraph(node_list)

    if len(list(subgraph.nodes)) == 0:
        #check if the graph is empty
        error_code = 204
    else:
        error_code = 200
    return subgraph,error_code

#Input: node_id_list, a list of int, a list of node id
#       relation_id_list, a list of int, a list of relation id
#       delete_node, a int, the node id of the deleted node
#       graph, a py2neo graph object
#Output: a subgraph object in py2neo after deletion
def graph_after_delete_node(node_id_list,relation_id_list,delete_node,graph):
    node_list = [graph.nodes.get(i) for i in node_id_list]
    relation_list = [graph.relationships.get(i) for i in relation_id_list]

    subgraph = Subgraph()
    subgraph = subgraph | Subgraph((),relation_list)
    subgraph = subgraph | Subgraph(node_list)
    for r in list(subgraph.relationships):
        if r.start_node.identity == delete_node:
            subgraph = subgraph - r | Subgraph([r.end_node])
        elif r.end_node.identity == delete_node:
            subgraph = subgraph - r | Subgraph([r.start_node])

    if len(list(subgraph.nodes)) == 0:
        #check if the graph is empty
        error_code = 204
    else:
        error_code = 200
    return subgraph,error_code

#Input: node_id_list, a list of int, a list of node id
#       relation_id_list, a list of int, a list of relation id
#       expand_node, a int, the node id of the expanded node
#       graph, a py2neo graph object
#       limit_number, a int, the maximum number of nodes we could add after expansion
#       relationship_name, a certain relationship we want to expand, if it is None then we just expand on random relationship
#Output: a subgraph object in py2neo after expansion
def graph_after_expand_node(graph,node_id_list,relation_id_list,expand_node,limit_number,relationship_name):
    node_list = [graph.nodes.get(i) for i in node_id_list]
    relation_list = [graph.relationships.get(i) for i in relation_id_list]

    #reconstruct the subgraph
    subgraph = Subgraph()
    subgraph = subgraph | Subgraph((),relation_list)
    subgraph = subgraph | Subgraph(node_list)

    #find the expanded relationship from the expand_node
    if relationship_name is None:
        #expand on random relationship
        new_sub = Subgraph((),graph.match({graph.nodes.get(expand_node)}).limit(limit_number).all())
    else:
        #expand on certain relationship
        new_sub = Subgraph((),graph.match({graph.nodes.get(expand_node)},relationship_name).limit(limit_number).all())
       
    #check for possible connection between the newly added node and old node
    new_node_id = [n.identity for n in list(new_sub.nodes)]
    if len(new_node_id) != 0:
        error_code = 200
        new_node_id.remove(expand_node)
        new_node_list = [graph.nodes.get(i) for i in new_node_id]
        comb_node_list = [graph.nodes.get(i) for i in node_id_list if i != expand_node]

        #find all possible pairs between new node and old new except the expanded one
        all_pairs = [set(comb) for comb in product(new_node_list, comb_node_list)] 

        #query the graph to see if there exists some relationships between all pair
        for pair in all_pairs:
            relation = graph.match(pair).first()
            if relation is not None:
                new_sub = new_sub | relation
    else:
        #new subgraph do not find new edges during expansion
        error_code = 204
    #concatenate the subgraph
    subgraph = subgraph | new_sub
    return subgraph,error_code

#Input: subgraph, a subgraph object in py2neo
#       graph, the entire neo4j graphDB
#       entity_identifier, a string, denotes the property name which you want to display in the front end (same as the mapping property)
#Ouput: a dictionary containing the graph in json format
def convert_subgraph_to_json_withR(subgraph,entity_identifier,graph):
    #construct list of node dicitionary 
    node_dict_list = []
    for n in list(subgraph.nodes):
        node_property = dict(n)
        node_property.update({"mapping":entity_identifier})
        relationship_types,_ = get_all_relationship_type(graph,n.identity)
        node_dict = {"id":n.identity,"labels":[],"relationship_types":relationship_types,"properties":node_property,"type":"node"}
        node_dict_list.append(node_dict)
    
    #construct list of relationship dicitionary
    relation_dict_list = []
    for r in list(subgraph.relationships):
        relation_property = dict(r)
        relation_property.update({"mapping":"relationship_type"})
        relation_property.update({"relationship_type":type(r).__name__})
        relation_dict = {"startNode":r.start_node.identity,"endNode":r.end_node.identity,
                         "id":r.identity,"label":[],"properties":relation_property}
        relation_dict_list.append(relation_dict)

    graph_dict = {"nodes":node_dict_list,"relationships":relation_dict_list}
    data_dict = {"graph":graph_dict}
    dict_result = {"results":[{"columns":[],"data":[data_dict]}]}
    return dict_result

#Input: subgraph, a subgraph object in py2neo
#       entity_identifier, a string, denotes the property name which you want to display in the front end (same as the mapping property)
#Ouput: a dictionary containing the graph in json format
def convert_subgraph_to_json(subgraph,entity_identifier):
    #construct list of node dicitionary 
    node_dict_list = []
    for n in list(subgraph.nodes):
        node_property = dict(n)
        node_property.update({"mapping":entity_identifier})
        node_dict = {"id":n.identity,"labels":[],"properties":node_property,"type":"node"}
        node_dict_list.append(node_dict)

    #construct list of relationship dicitionary
    relation_dict_list = []
    for r in list(subgraph.relationships):
        relation_property = dict(r)
        relation_property.update({"mapping":"relationship_type"})
        relation_property.update({"relationship_type":type(r).__name__})
        relation_dict = {"startNode":r.start_node.identity,"endNode":r.end_node.identity,
                         "id":r.identity,"label":[],"properties":relation_property}
        relation_dict_list.append(relation_dict)

    graph_dict = {"nodes":node_dict_list,"relationships":relation_dict_list}
    data_dict = {"graph":graph_dict}
    dict_result = {"results":[{"columns":[],"data":[data_dict]}]}
    return dict_result

#Input: node_id_list, a list of int, a list of node id
#       database, a string, denotes the name of graph database we will query
#       graph, a Py2neo graph object
#Ouput: a list of dictionary containing the county information for each nodes in the node_id_list 
def get_county_info_for_nodes(node_id_list,database,graph):
    output = []
    # different database have slightly different logic
    if database == "ppod":
        geoid_cypher = "match (n)-[p:in_county]-(m) where id(n)={} return m.geo_id,n.label"
        for node_id in node_id_list:
            cypher_result = graph.run(geoid_cypher.format(node_id)).data()
            county_list = list(set([i['m.geo_id'] for i in cypher_result]))
            if len(county_list)==0:
                node_name = None
                error_code = 202
            elif county_list[0] is None: 
                county_list = []
                node_name = None
                error_code = 202
            else:
                node_name = cypher_result[0]['n.label']
            county_dict = {"node_id":node_id,"node_name":node_name,"county_id":county_list}
            output.append(county_dict)
    elif database == "cfs":
        for node_id in node_id_list:
            node = graph.nodes.get(node_id)
            county_dict = {"node_id":node_id,"node_name":node['county'],"county_id":[node['id']]}
            output.append(county_dict)    
    error_code = 200
    return output,error_code

#Input:node_id, a int, a node id which we want to check for all relationship types
#      graph, a py2neo graph object
#Ouput: a dictionary where key is a relationship type name and the value is corresponding counter
def get_all_relationship_type(graph,node_id):
    cypher = "match (n)-[p]-(m) where id(n) = {0} return type(p) as type, count(p) as amount"
    cypher_result = graph.run(cypher.format(node_id)).data()
    if len(cypher_result) == 0:
        error_code = 204
    else:
        error_code = 200
    return {r["type"]: r["amount"] for r in cypher_result},error_code

def print_(tx, ):
    record = tx.run("""
        CALL apoc.export.json.all(null,{useTypes:true, stream: true})
        YIELD file, nodes, relationships, properties, data
        RETURN file, nodes, relationships, properties, data
    """)
    return [rr for rr in record]

#Input:graph, a py2neo subgraph object
#Ouput: a dictionary where key is a entity type name and the value is corresponding counter
#       a dictionary where key is a relationship type name and the value is corresponding counter
def get_graph_overview(graph,entity_type,relationship_type):
    entity_dist_dict = {}
    for n in entity_type:
        entity_dist_dict[n] = graph.nodes.match(n).__len__()

    relationship_dist_dict = {}
    for r in relationship_type:
        relationship_dist_dict[r] = graph.relationships.match(r_type=r).__len__()
    return_dict = {"entity":entity_dist_dict,"relationship":relationship_dist_dict}
    return return_dict

#Input:graph, a py2neo subgraph object
#      entity_type, a list of str, a list of entity type
#      limit_number, the limit for number of nodes per type
#Output: a subgraph object in py2neo after query certain type
def get_graph_with_certain_entity(graph,entity_type,limit_number):
    subgraph = Subgraph()
    for n in entity_type:
        subgraph = subgraph | Subgraph(list(graph.nodes.match(n).limit(limit_number).all()))
    if len(list(subgraph.nodes)) == 0:
        #check if the graph is empty
        error_code = 204
    else:
        error_code = 200
    return subgraph,error_code

#Input:graph, a py2neo subgraph object
#      relationship_type, a list of str, a list of relationship type
#      limit_number, the limit for number of relationship per type
#Output: a subgraph object in py2neo after query certain type
def get_graph_with_certain_relationship(graph,relationship_type,limit_number):
    subgraph = Subgraph()
    for r in relationship_type:
        subgraph = subgraph| Subgraph((),graph.relationships.match(r_type = r).limit(limit_number).all())
    if len(list(subgraph.nodes)) == 0:
        #check if the graph is empty
        error_code = 204
    else:
        error_code = 200
    return subgraph,error_code