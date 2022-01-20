from flask import Flask, jsonify, request,Response
from flask_cors import CORS
import json 
from helper import filterGraph
# configuration
DEBUG = True

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
    dados = [{
                'name': 'Teste',
                'age': 13
            }]
    options =  {
                'columns': [{
                    'title': 'Name',
                    'field': 'name',
                    'sorter': 'string',
                    'width': 200,
                    'editor': True,
                }, ]
            }
    output = {
        'data': dados,
        'option': options
    }
    return Response(json.dumps(output))
if __name__ == '__main__':
    app.run()