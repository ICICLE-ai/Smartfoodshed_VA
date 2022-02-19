from telnetlib import ENCRYPT
from flask import Flask, jsonify, request,Response
from neo4j import GraphDatabase, basic_auth
from flask_cors import CORS
import json
from neo4j import GraphDatabase
from py2neo import Graph
from py2neo import Subgraph
import py2neo
from helper import filterGraph, print_
# configuration
DEBUG = True
driver = None

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/getGraphData', methods=['GET'])
def getGraphData():
    f = open('../../../local_data/graph.json')
    data = json.load(f)
    # print(type(filtered_data))
    return Response(json.dumps(data))

@app.route('/getTableData', methods=['GET'])
def getTableData():
    f = open('../../../local_data/ppod_entity_table.json')
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

if __name__ == '__main__':
    
    # driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "123"))
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "123")) # This should be a global variable in this app
    schema = py2neo.database.Schema(graph)
    if len(list(schema.node_labels)) > 1:
        entity_identifier = "label" # This should be a global variable in this app
    else:
        entity_identifier = "county" # This should be a global variable in this app
    app.run()