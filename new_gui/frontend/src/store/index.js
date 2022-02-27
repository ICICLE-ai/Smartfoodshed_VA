import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import {generationEntityRelations, 
        addItemsToSelection, 
        removeItemsToSelection,
        idParsingToDict,
        retrieveInteractiveTable} from '@/utils/storehelp'
import {graphNodeLinkRemoval} from '@/utils/KGutils'
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
  }
}
const mutations = {
  SET_graphData (state, val) {
    state.graphData = val
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
    console.log("!!!!!!!!!!!!===========!!!!!!!!!!!!!")
    console.log(res)
  },
  RESET_GRAPHDATA(state, ){
    state.graphData = state.originalGraph
  },
  NODE_EXPAND(state, {node_id}){
    
  }, 
  NODE_REMOVE(state, {updatedGraphData}){
    state.graphData = updatedGraphData
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
  async retrieveGraphFromTable({commit, state}) {
    console.log("retrieve graph data from table") 
    // data preparation
    let {nodes, relations} = generationEntityRelations(state.tableSelected)
    const path = "http://127.0.0.1:5000/retrieveSubgraph"
    console.log(nodes, relations)
    const result = await axios.post(path, {nodes, relations})
    console.log("result returned back!!!")
    console.log(result)
    commit('SET_graphData', result['data'])
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
  node_expand({commit, state}, {node_id}){
    commit('NODE_EXPAND', {node_id})
  }, 
  node_remove({state, commit}, {node_id}){
    alert("node removal: " + node_id)
    const updatedGraphData = graphNodeLinkRemoval(state.graphData, node_id)
    commit('NODE_REMOVE', {updatedGraphData})

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
