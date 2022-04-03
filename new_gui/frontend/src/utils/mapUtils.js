import axios from 'axios'


async function loadMapInitialData(){
    const path = "..."
    const data = null
    const responseData = postRequest(path, data, {
        "204": "No content retrieved for initializing map", 
        "400": "Error in initializing map"
    })
    
    return responseData
}


async function queryMapInfoWithNode(node_list){
    const path = "..." 
    const data = {
        "node": node_list
    }
    const responseData = postRequest(path, data, {
        "204": "No content retrieved for selected node list", 
        "400": "Error in retrieve geo info for the selected nodes "
    }) 
    return responseData 
}

async function postRequest({url, data, warningMsg}) { 
    const response = await axios.post(url, data)
    const statusCode = response.status
    if (statusCode == "200") {
        return response['data'] 
    } else if (statusCode == "204") {
        alert(warningMsg['204'])
        return null
    } else {
        alert(warningMsg['400'])
        return null
    } 
}

export {loadMapInitialData, queryMapInfoWithNode}