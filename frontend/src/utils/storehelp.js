import { active } from "d3"

function getItemIndex(container, item){
    if (!container || container.length == 0){
        return -1
    }
    const indexingTerm = item.relation_id? 'relation_id': item.id? 'id': null
    if (indexingTerm == null){
        console.log("Error: item doesn't contain id or relation_id attribute")
        return -1
    }
    const numOfItems = container.length
    if (numOfItems > 0){
        for (let i = 0; i < numOfItems; i++) {
            if(container[i][indexingTerm] && item[indexingTerm]){
                if (container[i][indexingTerm] == item[indexingTerm]) {
                    return i
                }
            }
        }
    }else{
        return -1
    }
    return -1
}

function generationEntityRelations(container){
    const sheets = Object.keys(container)
    let nodes = []
    let relations = [] 
    sheets.forEach(sheet => {
        const data = container[sheet]
        const items = Object.values(data)
        items.forEach(item => {
            if(item.relation_id != null){
                relations.push(item.relation_id)
            }else if(item.id != null) {
                nodes.push(item.id)
            }else{
                console.log("Error, item doesn't have id or relation_id")
            }
        })
    })
    return {nodes, relations}
}

function addItemsToSelection(container, items){
    if (items.length <= 0) {
        return -1
    } else {
        const sample = items[0] 
        const indexingTerm = sample.relation_id!=null? 'relation_id': sample.id!=null? 'id': null
        items.forEach(item => {
            const id = item[indexingTerm]
            if(id != null) {
                if(container[id] == null){
                    container[id] = item
                }
            } else {
                console.log(item)
                console.log(id)
                console.log(id != null)
                console.log(indexingTerm)
                console.log("Error: item doesn't have either id or relation_id")
            }
        })
        return 1
    }
}

function removeItemsToSelection(container, items){
    if (items.length <= 0) {
        return -1
    } else {
        const sample = items[0] 
        const indexingTerm = sample.relation_id!=null? 'relation_id': sample.id!=null? 'id': null
        items.forEach(item => {
            const id = item[indexingTerm]
            if(id != null) {
                if(container[id] != null){
                    delete container[id]
                }
            } else {
                console.log("Error: Item id: " + id + " is not in container")
            }
        })
        return 1
    }
}

function idParsingToDict(container, {sheets, data}){
    if (container == null) {
        alert("container for id parsing is Null")
    }else {
        container['relations'] = {}
        container['entities'] = {} 
        sheets.forEach(sheet => {
            const sheetData = data[sheet]['tableData']
            sheetData.forEach(item=>{
                if(item.relation_id != null){
                    container['relations'][item.relation_id]={
                        fromSheet: sheet,
                        type: 'relationship',
                        data: item
                    }
                }else if(item.id != null){
                    container['entities'][item.id]={
                        fromSheet: sheet,
                        type: 'entity',
                        data: item
                    } 
                }else{
                    console.log('Item no id or relation id')
                }
            })
        })
    }
}

function retrieveInteractiveTable(tableData, dictionary, {entities, relations}){ 
    const sheets = tableData['sheet']
    let filtered_data = {}
    let activeSheets = []
    if (entities == null && relations == null){
        return null
    }
    console.log("---===---===---===---===")
    console.log(entities)
    console.log(relations)
    // entity handler
    if (entities != null && Object.keys(dictionary['entities']).length > 0) {
        entities.forEach(eId => {
            const info = dictionary['entities'][eId]
            if(info!=null){
                const originalSheet = info['fromSheet']
                if(!activeSheets.includes(originalSheet)){
                    activeSheets.push(originalSheet)
                }
                if(filtered_data[originalSheet]!=null){
                    filtered_data[originalSheet]['tableData'].push(info['data'])
                }else{
                    filtered_data[originalSheet] = {
                        'tableData': [info['data']], 
                        'tableInfo': tableData['data'][originalSheet]['tableInfo']
                    } 
                }
            }else {
                console.log(dictionary['entities'])
                console.log(dictionary['entities'][eId])
                console.log("missing info from dictionary")
            }
        })
    }
    // relation handler
    if (relations != null && Object.keys(dictionary['relations']).length > 0) {
        relations.forEach(rId => { 
            const info = dictionary['relations'][rId]
            if(info!=null){
                const originalSheet = info['fromSheet']
                if(!activeSheets.includes(originalSheet)){
                    activeSheets.push(originalSheet)
                }
                if(filtered_data[originalSheet]!=null){
                    filtered_data[originalSheet]['tableData'].push(info['data'])
                }else{
                    filtered_data[originalSheet] = {
                        'tableData': [info['data']], 
                        'tableInfo': tableData['data'][originalSheet]['tableInfo']
                    } 
                }
            }else {
                console.log("missing info from dictionary")
            }
        })
    }
    return {data:filtered_data, sheet: activeSheets}
}

export {getItemIndex, generationEntityRelations, addItemsToSelection, removeItemsToSelection, idParsingToDict, retrieveInteractiveTable}