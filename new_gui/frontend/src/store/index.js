import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import {generationEntityRelations, 
        addItemsToSelection, 
        removeItemsToSelection,
        idParsingToDict,
        retrieveInteractiveTable} from '@/utils/storehelp'
import {graphNodeLinkRemoval, 
        graphNodeLinkExpand} from '@/utils/KGutils'
Vue.use(Vuex)
function initialState () {
  return {
    graphData: null,
    tableData: null, // raw data
    originalGraph: null, 
    tableSelection: null,
    tableSelected: {},
    idDict: {},
    tableInteractiveMode: false, 
    interactiveTableData: null, 
    relationStatusReady: false, 
    relationTypeData: null,
  }
}
const mutations = {
  SET_graphData (state, val) {
    state.graphData = val
  },
  SET_GRAPHDATA_RELATION_TYPE_DATA(state, val){
    state.relationTypeData = val
  },
  SET_graphDataBackUp (state, val) {
    state.originalGraph = val
  },
  SET_tableData (state, val) {
    state.tableData = val
  },
  SET_tableSelection (state, val) {
    state.tableSelection = val
  },
  SET_TABLE_SELECTED_ADD (state, {sheetName, value}) {
    console.log("!!!!!!!")
    if(!state.tableSelected[sheetName]){
      state.tableSelected[sheetName] = {}  
    }  
    addItemsToSelection(state.tableSelected[sheetName], value)
  },
  SET_TABLE_SELECTED_REMOVE(state, {sheetName, value}) {
    removeItemsToSelection(state.tableSelected[sheetName], value)
  }, 
  TABLE_INTERACTIVE_ON(state, ) {
    state.tableInteractiveMode = true
  },
  TABLE_INTERACTIVE_OFF(state, ) {
    state.tableInteractiveMode = false
  },
  RESET_TABLE_SELECTED(state, ) {
    state.tableSelected = {}
  },
  UPDATE_INTERACTIVE_TABLE(state, {entities, relations}){ 
    const res = retrieveInteractiveTable(state.tableData, state.idDict, {entities, relations}) 
    if (res != null){
      state.interactiveTableData = res
    }else{
      alert("retrieve nothing")
    }
  },
  RESET_GRAPHDATA(state, ){
    state.graphData = state.originalGraph
  },
  NODE_EXPAND(state, {updatedGraphData}){
    state.graphData = updatedGraphData 
  }, 
  NODE_REMOVE(state, {updatedGraphData}){
    state.graphData = updatedGraphData
  },
  RELATION_STATUS_OFF(state,){
    state.relationStatusReady = false 
  },
  RELATION_STATUS_ON(state,){
    state.relationStatusReady = true
  }
}
const actions = {
  async getGraphData ({commit, dispatch, state}) {
    const path = 'http://127.0.0.1:5000/getGraphData'
    var result = await axios.get(path)
    commit('SET_graphData', result['data'])
    commit('SET_graphDataBackUp', result['data'])
  },
  async getTableData ({commit, dispatch, state}) {
    const path = 'http://127.0.0.1:5000/getTableData'
    var result = await axios.get(path)
    var tableSelection_temp = {}
    var sheet = result['data']['sheet'] // list of sheet name
    var data = result['data']['data'] // list of data obj
    sheet.forEach(s => {
      tableSelection_temp[s] = []
    })
    commit('SET_tableSelection', tableSelection_temp)
    commit('SET_tableData', result['data'])
    console.log("check table data again!!!")
    console.log(result['data'])
    idParsingToDict(state.idDict, {sheets: sheet, data: data})
  },
  setTableSelected ({commit, displatch, state}, {action, sheetName, value}) {
    console.log(action)
    if (action == "add") {
      commit('SET_TABLE_SELECTED_ADD', {sheetName, value})
    } else if (action == 'remove') {
      commit('SET_TABLE_SELECTED_REMOVE', {sheetName, value})
    } else {
      console.log("Waring! setTableSelected action received an invalid action type: " + action)
    }
  },
  retrieveGraphFromTable({commit, state}) {
    console.log("retrieve graph data from table") 
    // data preparation
    let {nodes, relations} = generationEntityRelations(state.tableSelected)
    const path_retrieve_graph = 'http://127.0.0.1:5000/retrieveSubgraph'
    const path_retrieve_graph_relation = 'http://127.0.0.1:5000/retrieveSubgraphWithR' 
    // set getDataRelationStatus to be false to indicate 
    commit('RELATION_STATUS_OFF')
    // retrieve data
    axios.post(path_retrieve_graph, {nodes, relations})
      .then(result => {
        console.log(result)
        commit('SET_graphData', result['data']) 
      })
      .catch(error => {
        console.log(error)
        console.log(error.response.status)
      })
    
      axios.post(path_retrieve_graph_relation, {nodes, relations})
        .then(result => {
          console.log("!!!!!!1---------!!!!!!!!!!!! relation data back ")
          console.log(result)
          commit('SET_GRAPHDATA_RELATION_TYPE_DATA', result['data'])  
          commit('RELATION_STATUS_ON')
        })
        .catch(error => {
          console.log(error)
          console.log(error.response.status)
        })

  },
  retrieveSubTable({commit, state}, {entities, relations}) { 
    console.log("retrieve sub table!!!")
    commit('TABLE_INTERACTIVE_ON')
    commit('UPDATE_INTERACTIVE_TABLE', {entities, relations})
    commit('RESET_TABLE_SELECTED')
  },
  resetTableGraph({commit, state}, ){
    commit('TABLE_INTERACTIVE_OFF') 
    commit('RESET_GRAPHDATA')
  },
  async node_expand({commit, state}, {node_id}){
    const updatedGraphData = await graphNodeLinkExpand(state.graphData, node_id)
    commit('NODE_EXPAND', {updatedGraphData: updatedGraphData['data']})
  }, 
  node_remove({state, commit}, {node_id}){
    const updatedGraphData = graphNodeLinkRemoval(state.graphData, node_id)
    commit('NODE_REMOVE', {updatedGraphData: updatedGraphData})
  }
}
export default new Vuex.Store({
  state: initialState,
  getters: {
  },
  mutations: mutations,
  actions: actions,
  modules: {
  }
})
