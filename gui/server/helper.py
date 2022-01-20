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

