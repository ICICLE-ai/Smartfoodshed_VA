from re import T
from telnetlib import ENCRYPT
from flask import Flask, jsonify, request,Response,redirect, make_response
from neo4j import GraphDatabase, basic_auth
from flask_cors import CORS
import json
from neo4j import GraphDatabase
from py2neo import Graph
import time
from py2neo import Subgraph
import py2neo
import pandas as pd
import requests
import os 
os.environ["APP_CONFIG_PATH"] = "./config.yaml"

import helper
from iciflaskn import icicle_flaskn
from iciflaskn import auth
from iciflaskn.config import config


""" config.py
// Adding config file to config your local data folder please !!!!!!!!!!!

// e.g.
localfile_path = "../../../local_data"
"""
# from config import localfile_path

localfile_path = "https://raw.githubusercontent.com/yasmineTYM/PPOD_KG/main/"
# localfile_path = "/Users/yameitu/Desktop/ICIRCLE/local_data/"
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


#app.register_blueprint(icicle_flaskn)

@app.route('/login', methods=['GET'])
def login():
    """
    Check for the existence of a login session, and if none exists, start the OAuth2 flow.
    """
    authenticated, _, _ = auth.is_logged_in()
    # if already authenticated, redirect to the root URL
    if authenticated:
        result = {'path':'/', 'code': 302}
        return result
    # otherwise, start the OAuth flow
    callback_url = f"{config['app_base_url']}/oauth2/callback"
    tapis_url = f"{config['tapis_base_url']}/v3/oauth2/authorize?client_id={config['client_id']}&redirect_uri={callback_url}&response_type=code"
    # print('no, not auth, redirect to:',tapis_url)
    result = {'path': tapis_url, 'code':302}
    return jsonify(result)


@app.route('/oauth2/callback', methods=['GET'])
def callback():
    """                                                                                                                                                                               
    Process a callback from a Tapis authorization server:
      1) Get the authorization code from the query parameters.
      2) Exchange the code for a token
      3) Add the user and token to the sessionhttps
      4) Redirect to the /data endpoint.
    """
    code = request.args.get('code')
    if not code:
        raise Exception(f"Error: No code in request; debug: {request.args}")
    url = f"{config['tapis_base_url']}/v3/oauth2/tokens"
    data = {
        "code": code,
        "redirect_uri": f"{config['app_base_url']}/oauth2/callback",
        "grant_type": "authorization_code",
    }
    try:
        response = requests.post(url, data=data, auth=(config['client_id'], config['client_key']))
        response.raise_for_status()
        json_resp = json.loads(response.text)
        token = json_resp['result']['access_token']['access_token']
    except Exception as e:
        raise Exception(f"Error generating Tapis token; debug: {e}")

    username = auth.get_username(token)
    
    response = make_response(redirect(os.environ['FRONT_URL'], code=302))

    domain = os.environ['FRONT_URL'][8:-1]
    response.set_cookie("token", token, domain=domain)
    response.set_cookie("username", username, domain=domain)
    
    return response

@app.route('/getGraphData', methods=['GET'])
def getGraphData():
    data = helper.readJsonFromGit(localfile_path+'input_graph.json')
    # print(type(filtered_data))
    return Response(json.dumps(data))

@app.route('/g', methods=['GET'])
def getMapData():
    global database
    data = helper.readJsonFromGit(localfile_path+database+'_map_initial_data.json')
    # with open('../../../local_data/'+database+"_map_initial_data_v1.json") as f:
    #     data = json.loads(f.read())
    output = {
        'data': data,
        'database': database
    }
    return Response(json.dumps(output))

@app.route('/getTableData', methods=['GET'])
def getTableData():
    ## Create a new py file config.py and add localfile_path to indicate the place of local_data folder
    ## This config file will not be pushed to the osu code, so we don't need to always change path
    # global database
    # print('gettabledata', database)
    data = helper.readJsonFromGit(localfile_path+database+'_table.json')

    # with open('../../../local_data/'+database+"_table_localserver.json") as f:
    #     data = json.loads(f.read())
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
    return Response(json.dumps(result))

@app.route('/retrieveSubgraph', methods=['POST'])
def getSubGraphFromTable(): 
    request_obj = request.get_json()
    nodes_list = []
    relation_list = []
    dict_res = {}
    try:
        if request_obj.get("nodes") is not None: 
            nodes_list = request_obj.get("nodes")
        
        if request_obj.get("relations") is not None:
            relation_list = request_obj.get("relations")
        attempts  = 0
        while attempts<3:
            try:
                subgraph_res,error_code = helper.get_subgraph(graph, nodes_list, relation_list)
                dict_res = helper.convert_subgraph_to_json(subgraph_res, entity_identifier,database,fips)
                break
            except:
                attempts+=1
        # print(error_code)
    except Exception as e:
        print(f"404 - {e}")
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/retrieveSubgraphWithR', methods=['POST'])
def getSubGraphFromTableWithR(): 
    request_obj = request.get_json()
    nodes_list = []
    relation_list = []
    dict_res = {}
    try:
        if request_obj.get("nodes") is not None: 
            nodes_list = request_obj.get("nodes")
        
        if request_obj.get("relations") is not None:
            relation_list = request_obj.get("relations")
        attempts = 0
        while attempts<3:
            try:
                subgraph_res,error_code = helper.get_subgraph(graph, nodes_list, relation_list)
                dict_res = helper.convert_subgraph_to_json_withR(subgraph_res, entity_identifier,graph,database,fips)
                break
            except:
                attempts+=1
    except Exception as e:
        print(f"404 - {e}")
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)


@app.route('/deleteNode', methods=['POST'])
def delete_node_from_graph():
    request_obj = request.get_json()
    nodes_list = []
    relation_list = []
    dict_res = {}
    try:
        if request_obj.get("nodes") is not None:
            nodes_list = request_obj.get("nodes")
        if request_obj.get("relations") is not None:
            relation_list = request_obj.get("relations")
        if request_obj.get("delete_node") is not None:
            delete_node = request_obj.get("delete_node")

        subgraph_res,error_code = helper.graph_after_delete_node(nodes_list,relation_list,delete_node,graph)

        dict_res = helper.convert_subgraph_to_json(subgraph_res, entity_identifier,graph,database,fips)
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
    dict_res = {}
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
        attempts = 0
        while attempts<3:
            try:
                subgraph_res,error_code = helper.graph_after_expand_node(graph,nodes_list,relation_list,expand_node,limit_number,relationship_name,database)
                dict_res = helper.convert_subgraph_to_json(subgraph_res, entity_identifier,database,fips)
                break
            except:
                attempts+=1
    except Exception as e:
        print(f"404 - {e}")
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
    dict_res = {}
    # limit_number = 5
    # try:
    if request_obj.get("nodes") is not None:
        nodes_list = request_obj.get("nodes")
    if request_obj.get("relations") is not None:
        relation_list = request_obj.get("relations")
    if request_obj.get("expand_node") is not None:
        expand_node = request_obj.get("expand_node")
    if request_obj.get("limit_number") is not None:
        limit_number = request_obj.get("limit_number")
    relationship_name = request_obj.get("relationship_name")
    attempts = 0
    while attempts<3:
        try:
            subgraph_res,error_code = helper.graph_after_expand_node(graph,nodes_list,relation_list,expand_node,limit_number,relationship_name,database)
            dict_res = helper.convert_subgraph_to_json_withR(subgraph_res, entity_identifier,graph,database,fips)
            break
        except:
            attempts+=1
    # except:
    #     error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/getRType', methods=['POST'])
def get_all_relationship_types():
    request_obj = request.get_json()
    dict_res = {}
    try:
        if request_obj.get("node") is not None:
            node = request_obj.get("node")
        dict_res,error_code = helper.get_all_relationship_type(graph,node)
    except Exception as e:
        print(f"404 - {e}")
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/getGraphOverview', methods=['GET'])
def get_graph_overview():
    return Response(json.dumps(graph_overview))

@app.route('/getGwithEntityType', methods=['POST'])
def get_graph_with_certain_entity():
    request_obj = request.get_json()
    limit_number = 3
    dict_res = {}
    try:
        print(request_obj)
        if request_obj.get("entity_type") is not None:
            entity_type = request_obj.get("entity_type")
            print(entity_type)
        subgraph_res,error_code = helper.get_graph_with_certain_entity(graph,entity_type,limit_number)
        dict_res = helper.convert_subgraph_to_json_withR(subgraph_res,entity_identifier,graph,database,fips)
    except Exception as e:
        print("Error!!!!!")
        print(f"404 - {e}")
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/getGwithRelationshipType', methods=['POST'])
def get_graph_with_certain_relationship():
    request_obj = request.get_json()
    limit_number = 3
    dict_res = {}
    try:
        print(request_obj)
        if request_obj.get("relationship_type") is not None:
            relationship_type = request_obj.get("relationship_type")
        subgraph_res,error_code = helper.get_graph_with_certain_relationship(graph,relationship_type,limit_number)
        dict_res = helper.convert_subgraph_to_json_withR(subgraph_res,entity_identifier,graph,database,fips)
    except:
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/getCountyInfo', methods=['POST'])
def get_county_info():
    request_obj = request.get_json()
    dict_res = {}
    try:
        if request_obj.get("node") is not None:
            node = request_obj.get("node")
        dict_res,error_code = helper.get_county_info_for_nodes(node,database,graph)
    except Exception as e:
        print(f"404 - {e}")
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/getEcoregionInfo', methods=['POST'])
def get_ecoregion_info():
    request_obj = request.get_json()
    dict_res = {}
    try:
        if request_obj.get("node") is not None:
            node = request_obj.get("node")
        dict_res,error_code = helper.get_ecoregion_info_for_nodes(node,database,graph)
    except Exception as e:
        print(f"404 - {e}")
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)

@app.route('/countyToNodes', methods=['POST'])
def get_associated_node_from_county():
    request_obj = request.get_json()
    dict_res = {}
    limit_number = 5
    try:
        if request_obj.get("county_id") is not None:
            county_id = request_obj.get("county_id")
        subgraph_res,error_code = helper.get_associated_nodes_for_county(county_id,database,graph,limit_number)
        dict_res = helper.convert_subgraph_to_json_withR(subgraph_res,entity_identifier,graph,database,fips)
    except Exception as e:
        print(f"404 - {e}")
        error_code = 404
    return Response(json.dumps(dict_res),status = error_code)


@app.route('/changeDataBase', methods=['POST'])
def changeDataBase():
    request_obj = request.get_json()
    global graph, entity_identifier,graph_overview,database,fips
    database = request_obj['database']
    if database=="ppod":
        graph = G1
        database = "ppod"
        entity_identifier = "label"
    elif database=="cfs":
        graph= G2
        database = "cfs"
        entity_identifier = "county"
    elif database=="ci":
        graph =  G3
        database = "ci"
        entity_identifier = "name"
    
    schema = py2neo.database.Schema(graph)
    attempts = 0
    while attempts<3:
        try:
            entity_type = list(schema.node_labels)
            relationship_type = list(schema.relationship_types)
            break 
        except:
            attempts+=1
    if len(entity_type) > 1:
        try:
            entity_type.remove("Resource")
        except:
            print('No Resource Entity type') 
        try:
            entity_type.remove("_GraphConfig")
        except:
            print("No _GraphConfig Entity Type") 
    
    graph_overview = helper.get_graph_overview(graph,entity_type,relationship_type)

    fips = pd.read_csv(localfile_path+"county_fips.csv")
    fips = fips.astype({"fips": str})
    fips['fips'] = fips['fips'].apply(lambda x: x.zfill(5))
    # fips = fips.append({'fips':'46102', 'name':'Oglala Lakota County','state':'SD'},ignore_index=True)
    fips.loc[len(fips)] = ['46102','Oglala Lakota County','SD']
    # fips = pd.concat(fips, to_add, axis=1)
    return Response(json.dumps({}), status=200)

def loadPPOD(graph, deleteOld=False):
    if deleteOld:
        c1 = "match (a) -[r] -> () delete a, r"
        c2 = "match (a) delete a"
        graph.run(c1)
        graph.run(c2)
#     graph.run('CREATE CONSTRAINT n10s_unique_uri ON (r:Resource) ASSERT r.uri IS UNIQUE')
    graph.run('CALL n10s.graphconfig.init();')
    graph.run('CALL n10s.graphconfig.init({ handleVocabUris: "IGNORE" })')
    graph.run("CALL apoc.import.graphml('https://raw.githubusercontent.com/yasmineTYM/PPOD_KG/main/PPOD_v9.graphml', {storeNodeIds:True, readLabels: True})")
    result = graph.run("MATCH (n) RETURN count(n) as num")
    for record in result:
        print(f"Number of nodes in the database: {record['num']}")
    result = graph.run("MATCH (n)-[r]->() RETURN COUNT(r) as num")
    for record in result:
        print(f"Number of edges in the database: {record['num']}")

if __name__ == '__main__':
    global G1, G2, G3
    ## local 
    # G1 = Graph("bolt://localhost:7687", auth=("neo4j", "123"), name="ppod")
    # G2 = Graph("bolt://localhost:7687", auth=("neo4j", "123"), name="cfs")
    # G1 = Graph("bolt://va1-neo4j:7687", auth=("neo4j", "newPassword"), name="ppod")
    # G2 = Graph("bolt://va1-neo4j:7687", auth=("neo4j", "newPassword"), name="cfs")
    # G3 = Graph("bolt+s://catalog.pods.icicle.tapis.io:443", auth=("catalog","d"), name="neo4j")
    ## server test 
    # G1 = Graph("bolt+ssc://neo1.pods.tacc.develop.tapis.io:443", auth=("neo1", "pass1"), secure=True, verify=False)
    # G2 = Graph("bolt+ssc://neo2.pods.tacc.develop.tapis.io:443", auth=("neo2", "pass2"), secure=True, verify=False)

    ## Read in environment variables to instantiate global Neo4j drivers named G1, G2, ..., GX
    ## Getting "sets" of credentials for each database.
    # db_creds = db_url1, db_user1, db_password1, db_url2, and so on. Can give as many credentials as wanted.
    # credentials
    creds = {}
    cred_set = 1
    while True:
        print(f"Attempting to parse through cred set {cred_set}")
        url = os.getenv(f"db_url{cred_set}")
        user = os.getenv(f"db_user{cred_set}")
        password = os.getenv(f"db_password{cred_set}")

        # There is no values for this "cred set"
        if not (url and user and password):
            break

        # Ensure the credential set has url, user, and password defined
        if not (url or user or password):
            msg = (f"Environment variable cred set {cred_set} has None for one of the following required variables:\n",
                   f"db_user{cred_set}: {url}",
                   f"db_user{cred_set}: {user}",
                   f"db_password{cred_set}: {password}")
            print(msg)
            raise ValueError(msg)

        creds.update({f"db_url{cred_set}": url,
                      f"db_user{cred_set}": user,
                      f"db_password{cred_set}": password})
        
        cred_set = cred_set + 1

    # This is hackery, this entire env fetching should be redone later, needed error message now for developers.
    # Did not get any creds
    if cred_set == 1:
        msg = f"At least one set of db credentials are required, env variables needed: db_url1, db_user1, and db_password1.\n"
        print(msg)
        raise ValueError(msg)
    elif cred_set == 2:
        msg = f"Only got one set of credentials, will use cred 1 for database 2 and 3."
        print(msg)
        creds["db_url2"] = creds["db_url1"]
        creds["db_url3"] = creds["db_url1"]
        creds["db_user2"] = creds["db_user1"]
        creds["db_user3"] = creds["db_user1"]
        creds["db_password2"] = creds["db_password1"]
        creds["db_password3"] = creds["db_password1"]
    elif cred_set == 3:
        msg = f"Got two sets of credentials, will use cred 1 for database 3."
        print(msg)
        creds["db_url3"] = creds["db_url1"]
        creds["db_user3"] = creds["db_user1"]
        creds["db_password3"] = creds["db_password1"]
    else:
        pass


    error = None
    attempts = 0
    print(f"Attempting to connect to database.")
    while attempts < 10:
        try:
            G1 = Graph(creds['db_url1'], auth=(creds['db_user1'], creds['db_password1']))
            print("Successfully connected to G1.")
            G2 = Graph(creds['db_url2'], auth=(creds['db_user2'], creds['db_password2']))
            print("Successfully connected to G2.")
            G3 = Graph(creds['db_url3'], auth=(creds['db_user3'], creds['db_password3']))
            print("Successfully connected to G3.")
            print("Databases connected successfully!")
            break
        except Exception as e:
            print(f"{attempts} of 10 attempts: Couldn't connect to db, might be initializing, trying again in 5 seconds")
            time.sleep(5)
            attempts = attempts + 1
            error = e
    else:
        msg = f"Couldn't connect to db after 10 attempts with 5 seconds between attempts. last error e: {error}"
        print(msg)
        raise RuntimeError(msg)

    # For local develop, load ppod data into local db.
    local_run_db_init = os.getenv(f"local_run_db_init", False)
    if local_run_db_init:
        print(f"local_run_db_init env var was set , initializing database")
        if cred_set == 2:
            msg = f"Only got one set of credentials, will initialize db 1 with PPOD data."
            print(msg)
            loadPPOD(G1, True)
        elif cred_set == 3:
            msg = f"Got two sets of credentials, will initialize db 1 and 2 with PPOD data."
            print(msg)
            loadPPOD(G1, True)
            loadPPOD(G2, True)
        else:
            msg = f"Got three sets of credentials (or more), will initialize db 1, 2, and 3 with PPOD data."
            print(msg)
            loadPPOD(G1, True)
            loadPPOD(G2, True)
            loadPPOD(G3, True)

    app.secret_key = 'super secret key'
    app.run(host="0.0.0.0", debug=os.getenv("flask_debug", False))
