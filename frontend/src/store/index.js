import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import * as d3 from 'd3'
// var https = require('https');
import menu from '@/store/modules/menu.js'
import { base_request_url,apiClient } from '@/utils/base_url'
import {generationEntityRelations, 
        addItemsToSelection, 
        removeItemsToSelection,
        idParsingToDict,
        checkStatus,
        retrieveInteractiveTable} from '@/utils/storehelp'
import {graphNodeLinkRemoval, 
        graphNodeLinkExpand, 
        retrieveNodeLinkWithType} from '@/utils/KGutils'
import {
        loadMapInitialData, getNode,
        queryMapInfoWithNode} from '@/utils/mapUtils'
Vue.use(Vuex)
function initialState () {
  return {
    BETA_ROUTE: {'name': 'DashboardBeta', 'route': '/dashboard-beta'}, 
    DASH_ROUTE: {'name': 'Dashboard', 'route': '/'}, 
    graphData: null,
    DATABASE_NAME: null, // ppod or cfs 
    tableData: null, // raw data
    originalGraph: null, 
    tableSelection: null,
    tableSelected: {},
    idDict: {},
    tableInteractiveMode: false, 
    interactiveTableData: null, 
    relationStatusReady: false, 
    relationTypeData: null,
    loading: false,
    us: null,
    // ecoregion: null,
    expandThreshold: 5, // node expand limit 
    graphOverview: null, // for link overview 
    mapInitialInfo: null, 
    mapQueryInfo: null, 
    mapInQueryStatus: false,  
    activeTab: 0, 
    currentDragging: null,
    tableContainer: {
      height: 1000
    }, 
    colorMapping: {

    },
    // base_request_url: "http://127.0.0.1:5000/"
    // base_request_url: 'https://vaapi.develop.tapis.io/'
    database: "", //ppod or cfs 
  }
}
const mutations = {
  SET_DATABASE(state, val){
    state.database = val 
  },
  SET_DATABASE_NAME(state, val){
    state.DATABASE_NAME = val
  },
  SET_graphOverview(state, val){
    state.graphOverview = val
  },
  SET_expandThreshold(state, val){
    state.expandThreshold = val
  },
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
    // console.log("!!!!!!!")
    if(!state.tableSelected[sheetName]){
      state.tableSelected[sheetName] = {}  
    }  
    // addItemsToSelection(state.tableSelected[sheetName], value)
    if(value.length<=0){
      return -1
    }else{
      state.tableSelected[sheetName] = {}
      const sample = value[0]
      const indexingTerm = sample.relation_id!=null? 'relation_id': sample.id!=null? 'id': null
      value.forEach(item=>{
        const id = item[indexingTerm]
        if(id != null) {
            if(state.tableSelected[sheetName][id] == null){
              state.tableSelected[sheetName][id] = item
            }
        } else {
            console.log(item)
            console.log(id)
            console.log(id != null)
            console.log(indexingTerm)
            console.log("Error: item doesn't have either id or relation_id")
        }
      })
      // return 1
    }
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
  RELATION_STATUS_COUNTY(state,){
    state.relationStatusReady = 'fromMap'
  },
  RELATION_STATUS_OFF(state,){
    state.relationStatusReady = false 
  },
  RELATION_STATUS_ON(state,){
    state.relationStatusReady = true
  },
  SET_LOADING(state,data){
    state.loading = data 
  },
  LOADIN_MAP(state, us){
    state.us = us; 
  }, 
  LOADIN_MAP_DATA(state, mapInfo){
    state.mapInitialInfo = mapInfo
  }, 
  MAP_IN_QUERY(state, ) {
    state.mapInQueryStatus = true 
  }, 
  MAP_OFF_QUERY(state, ) {
    state.mapInQueryStatus = false
  }, 
  LOAD_QUERY_MAP_INFO(state, queryRes) {
    state.mapQueryInfo = queryRes
  },
  ACTIVE_TAB(state, activeTab){
    state.activeTab = activeTab
  },
  SET_CRRENTDRAGGING(state, vm){
    state.currentDragging = vm;
  },
  UPDATE_COLOR_MAPPING(state, {label, color}) {
    state.colorMapping[label] = color
  }
}
const actions = {
  changeDB({commit, dispatch, state}, data){
    commit('SET_DATABASE', data['database'])
    // var result = await apiClient.post("/changeDataBase", data)
    const path = base_request_url+'/changeDataBase' 
    axios.post(path, data)
      .then(result => {
        console.log('yes, loaded')
      })
      .catch(error => {
        alert(error+',Internal Server Error. Please refresh the page')
      })
  },
  async setExpandTh ({commit, dispatch, state}, data){
    commit('SET_expandThreshold', data)
  },
  async getGraphData ({commit, dispatch, state}) {
    const path = base_request_url+'getGraphData'
    var result = await axios.get(path)
    commit('SET_graphData', result['data'])
    commit('SET_graphDataBackUp', result['data'])
   
  },
  async getGraphOverview({commit, dispatch, state}){
    axios.get(base_request_url+"getGraphOverview").then(result=>{
      commit('SET_graphOverview', result)
    })
  },
  getTableData ({commit, dispatch, state}) {
    commit('SET_LOADING', true)
    const path = base_request_url+'getTableData'
    axios.get(path)
    .then(result=>{
      var tableSelection_temp = {}
      var sheet = result['data']['sheet'] // list of sheet name
      var data = result['data']['data'] // list of data obj
      sheet.forEach(s => {
        tableSelection_temp[s] = []
      })
      commit('SET_tableSelection', tableSelection_temp)
      commit('SET_tableData', result['data'])
      commit('SET_LOADING', false)
      console.log("check table data again!!!")
      console.log(result['data'])
      idParsingToDict(state.idDict, {sheets: sheet, data: data})
    })
    .catch(error=>{
      alert(error+',Internal Server Error. Please refresh the page')
    })
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
    commit('SET_LOADING', true)
    // data preparation
    let {nodes, relations} = generationEntityRelations(state.tableSelected)
    const path_retrieve_graph = base_request_url+'retrieveSubgraph'
    const path_retrieve_graph_relation = base_request_url+'retrieveSubgraphWithR' 
    // set getDataRelationStatus to be false to indicate 
    commit('RELATION_STATUS_OFF')
    // retrieve data
    axios.post(path_retrieve_graph, {nodes, relations})
      .then(result => {
        console.log(result)
        commit('SET_LOADING', false)
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
        commit('SET_LOADING', false)
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
  async node_expand({commit, state}, {node_id, relation}){
    
    commit('SET_LOADING', true)
    const updatedGraphData = await graphNodeLinkExpand(state.graphData, node_id, relation, state.expandThreshold)
    commit('SET_LOADING', false)
    if (updatedGraphData.status == 200){
      commit('NODE_EXPAND', {updatedGraphData: updatedGraphData['data']})
      commit('SET_GRAPHDATA_RELATION_TYPE_DATA', updatedGraphData['data']) 
    } else {
      alert("Expansion not successful")
    }
     
  }, 
  node_remove({state, commit}, {node_id}){
    const updatedGraphData = graphNodeLinkRemoval(state.graphData, node_id)
    commit('NODE_REMOVE', {updatedGraphData: updatedGraphData})
  },
  async load_map({state, commit}) {
   
    // load map geo data
    // const us = await d3.json('https://raw.githubusercontent.com/chrisdaly/map-data/master/us-counties.topojson.txt')
    // var us = {'test':'test'}
    // const us = await d3.json('../assets/us-countries.topojson.txt')
    // load map detail data 
    // commit("LOADIN_MAP", us)
    const mapInitialInfo = await loadMapInitialData(); 
    if (mapInitialInfo != null) {
      // 
      commit ("LOADIN_MAP_DATA", mapInitialInfo['data'])
      commit('SET_DATABASE_NAME', mapInitialInfo['database'])
    }
    
  },
  async retrieveNodesLinksWithTypes({state, commit}, {entity_type, relationship_type}){
    commit('SET_LOADING', true)
    const updatedGraphData = await retrieveNodeLinkWithType(entity_type, relationship_type)
    commit('SET_LOADING', false)
    if (updatedGraphData.status == 200){
      commit('NODE_EXPAND', {updatedGraphData: updatedGraphData['data']})
      commit('SET_GRAPHDATA_RELATION_TYPE_DATA', updatedGraphData['data']) 
      commit('RELATION_STATUS_ON')
    } else {
      alert("Expansion not successful")
    }
  }, 
  async retrieveNodeGeo({commit}, {node}){
    console.log("Check node info")
    commit("MAP_IN_QUERY") 
    if (node != null) {
      console.log(node)
      const mapInfo = await queryMapInfoWithNode(node)
      console.log(mapInfo)
      if (mapInfo != null) {
        commit ("LOAD_QUERY_MAP_INFO", mapInfo)
      }
    }
  },
  active_tab({commit}, activeTab) {
    commit("ACTIVE_TAB", activeTab)
  }, 
  changeCurrentDraggingVM({commit}, vm){
    commit('SET_CRRENTDRAGGING', vm)
  },
  containerSizeChange({commit, state}, {container, height}){
    state.tableContainer.height = height
  },
  async county2node({commit}, nodeid){
    var result = await getNode(nodeid)
    console.log(result)
    // commit('RELATION_STATUS_OFF')
    commit('SET_graphData', result['data']) 
    commit('RELATION_STATUS_COUNTY')
  }, 
  updateColorMapping({commit}, {label, color}){
    commit('UPDATE_COLOR_MAPPING', {label, color})
  }
}
export default new Vuex.Store({
  state: initialState,
  getters: {
  },
  mutations: mutations,
  actions: actions,
  modules: {
    menu,
  }
})
