from telnetlib import ENCRYPT
from flask import Flask, jsonify, request,Response
from neo4j import GraphDatabase, basic_auth
from flask_cors import CORS
import json
from neo4j import GraphDatabase
from py2neo import Graph
from py2neo import Subgraph
import py2neo
""" config.py
// Adding config file to config your local data folder please !!!!!!!!!!!

// e.g.
localfile_path = "../../../local_data"
"""
from config import localfile_path
import helper
# configuration
DEBUG = True
GRAPH_DRIVER = None
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# graph = None 

# entity_identifier = None
# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/getGraphData', methods=['GET'])
def getGraphData():
    f = open(f'{localfile_path}/input_graph.json')
    # f = open('../../../local_data/graph.json')
    data = json.load(f)
    # print(type(filtered_data))
    return Response(json.dumps(data))

@app.route('/g', methods=['GET'])
def getMapData():
    global database
    f = open(f'{localfile_path}/'+database+'_map_initial_data.json')
    # f = open(f'{localfile_path}/cfs_map_initial_data.json')

    # f = open('../../../local_data/graph.json')
    data = json.load(f)
    # print(type(filtered_data))
    return Response(json.dumps(data))

@app.route('/getTableData', methods=['GET'])
def getTableData():
    ## Create a new py file config.py and add localfile_path to indicate the place of local_data folder
    ## This config file will not be pushed to the osu code, so we don't need to always change path
    # f = open('../../../local_data/cfs_relation_table.json')
    f = open(f'{localfile_path}/ppod_table.json')
    data = json.load(f)
    output = {} ## tableName: {tableData:{}, tableInfo:{}}
    tableNames = []
    for ele in data:
        tableNames.append(ele['table_name'])
        output[ele['table_name']] = {
            'tableData': ele['table_data'],
            'tableInfo': ele['table_info']
        }
    result = {
        'data': output,
        'sheet': tableNames
    }
    # data = data.fillna('')
    # print(data.columns)

    # dados = data.to_dict('records')
    # output = {
    #     'data': dados,
    # }
    # print(data.keys())
    return Response(json.dumps(result))

@app.route('/retrieveSubgraph', methods=['POST'])
def getSubGraphFromTable(): 
    request_obj = request.get_json()
    nodes_list = []
    relation_list = []
    try:
        if request_obj.get("nodes") is not None: 
            nodes_list = request_obj.get("nodes")
        
        if request_obj.get("relations") is not None:
            relation_list = request_obj.get("relations")
        subgraph_res,error_code = helper.get_subgraph(graph, nodes_list, relation_list)
        dict_res = helper.convert_subgraph_to_json(subgraph_res, entity_identifier)
        print(error_code)
    except:
        print("404")
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/retrieveSubgraphWithR', methods=['POST'])
def getSubGraphFromTableWithR(): 
    request_obj = request.get_json()
    nodes_list = []
    relation_list = []
    try:
        if request_obj.get("nodes") is not None: 
            nodes_list = request_obj.get("nodes")
        
        if request_obj.get("relations") is not None:
            relation_list = request_obj.get("relations")
        subgraph_res,error_code = helper.get_subgraph(graph, nodes_list, relation_list)
        dict_res = helper.convert_subgraph_to_json_withR(subgraph_res, entity_identifier,graph)
    except:
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)


@app.route('/deleteNode', methods=['POST'])
def delete_node_from_graph():
    request_obj = request.get_json()
    nodes_list = []
    relation_list = []
    try:
        if request_obj.get("nodes") is not None:
            nodes_list = request_obj.get("nodes")
        if request_obj.get("relations") is not None:
            relation_list = request_obj.get("relations")
        if request_obj.get("delete_node") is not None:
            delete_node = request_obj.get("delete_node")

        subgraph_res,error_code = helper.graph_after_delete_node(nodes_list,relation_list,delete_node,graph)

        dict_res = helper.convert_subgraph_to_json(subgraph_res, entity_identifier,graph)
    except:
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/expandNode', methods=['POST'])
def expand_node():
    request_obj = request.get_json()
    nodes_list = []
    relation_list = []
    # default for limit number is 5
    limit_number = 5
    try:
        if request_obj.get("nodes") is not None:
            nodes_list = request_obj.get("nodes")
        if request_obj.get("relations") is not None:
            relation_list = request_obj.get("relations")
        if request_obj.get("expand_node") is not None:
            expand_node = request_obj.get("expand_node")
        if request_obj.get("limit_number") is not None:
            limit_number = request_obj.get("limit_number")
        relationship_name = request_obj.get("relationship_name")
        # print(nodes_list)
        # print(relation_list)
        # print(expand_node)
        subgraph_res,error_code = helper.graph_after_expand_node(graph,nodes_list,relation_list,expand_node,limit_number,relationship_name)
        dict_res = helper.convert_subgraph_to_json(subgraph_res, entity_identifier)
    except:
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/expandNodeWithR', methods=['POST'])
def expand_node_with_relationship_type():
    request_obj = request.get_json()
    nodes_list = []
    relation_list = []
    # default for limit number is 5
    limit_number = request_obj['threshold']
    print(limit_number)
    # limit_number = 5
    try:
        if request_obj.get("nodes") is not None:
            nodes_list = request_obj.get("nodes")
        if request_obj.get("relations") is not None:
            relation_list = request_obj.get("relations")
        if request_obj.get("expand_node") is not None:
            expand_node = request_obj.get("expand_node")
        if request_obj.get("limit_number") is not None:
            limit_number = request_obj.get("limit_number")
        relationship_name = request_obj.get("relationship_name")
        # print(nodes_list)
        # print(relation_list)
        # print(expand_node)
        subgraph_res,error_code = helper.graph_after_expand_node(graph,nodes_list,relation_list,expand_node,limit_number,relationship_name)
        dict_res = helper.convert_subgraph_to_json_withR(subgraph_res, entity_identifier,graph)
    except:
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/getRType', methods=['POST'])
def get_all_relationship_types():
    request_obj = request.get_json()
    try:
        if request_obj.get("node") is not None:
            node = request_obj.get("node")
        dict_res,error_code = helper.get_all_relationship_type(graph,node)
    except:
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/getGraphOverview', methods=['GET'])
def get_graph_overview():
    return Response(json.dumps(graph_overview))

@app.route('/getGwithEntityType', methods=['POST'])
def get_graph_with_certain_entity():
    request_obj = request.get_json()
    limit_number = 3
    try:
        print(request_obj)
        if request_obj.get("entity_type") is not None:
            entity_type = request_obj.get("entity_type")
            print(entity_type)
        subgraph_res,error_code = helper.get_graph_with_certain_entity(graph,entity_type,limit_number)
        dict_res = helper.convert_subgraph_to_json_withR(subgraph_res,entity_identifier,graph)
    except:
        print("Error!!!!!")
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/getGwithRelationshipType', methods=['POST'])
def get_graph_with_certain_relationship():
    request_obj = request.get_json()
    limit_number = 3
    try:
        print(request_obj)
        if request_obj.get("relationship_type") is not None:
            relationship_type = request_obj.get("relationship_type")
        subgraph_res,error_code = helper.get_graph_with_certain_relationship(graph,relationship_type,limit_number)
        dict_res = helper.convert_subgraph_to_json_withR(subgraph_res,entity_identifier,graph)
    except:
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/getCountyInfo', methods=['POST'])
def get_county_info():
    request_obj = request.get_json()
    try:
        print(request_obj)
        if request_obj.get("node") is not None:
            node = request_obj.get("node")
        dict_res,error_code = helper.get_county_info_for_nodes(node,database,graph)
        print(dict_res)
    except:
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

if __name__ == '__main__':
    global graph, entity_identifier,graph_overview,database
    # driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "123"))
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "123")) # This should be a global variable in this app
    schema = py2neo.database.Schema(graph)
    entity_type = list(schema.node_labels)
    relationship_type = list(schema.relationship_types)
    if len(entity_type) > 1:
        entity_type.remove("Resource")
        entity_type.remove("_GraphConfig")


    
    graph_overview = helper.get_graph_overview(graph,entity_type,relationship_type)
    if len(entity_type) > 1:
        database = "ppod"
        entity_identifier = "label" # This should be a global variable in this app
    else:
        database = "cfs"
        entity_identifier = "county" # This should be a global variable in this app
    app.run()
