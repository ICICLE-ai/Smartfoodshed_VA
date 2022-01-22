from telnetlib import ENCRYPT
from flask import Flask, jsonify, request,Response
from neo4j import GraphDatabase, basic_auth
from flask_cors import CORS
import json 
import pandas as pd
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
    f = open('all_converted.json')
    # f = open('./data/all_converted.json')
    data = json.load(f)

    num = 20
    sort = 'betweenness'

    # print(num, sort)
    filtered_data = filterGraph(data, num, sort)
    # print(type(filtered_data))
    return Response(json.dumps(filtered_data))

@app.route('/getTableData', methods=['GET'])
def getTableData():
    data = pd.read_csv('data/PPOD_PeopleOrg.csv')
    print(data.columns)
    dados = [{
                'name': 'Teste',
                'age': 13
            }]
    options =  {
                'columns': [{
                    'title': 'Name',
                    'field': 'name',
                },{
                    'title': 'Age',
                    'field': 'age'
                } ]
            }
    
    output = {
        'data': dados,
        'option': options,
        # 'temp': res
    }
    
    return Response(json.dumps(output))

if __name__ == '__main__':
    
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "123"))
    app.run()