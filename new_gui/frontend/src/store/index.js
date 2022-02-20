import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
Vue.use(Vuex)
function initialState () {
  return {
    graphData: null,
    tableData: null, // raw data

    tableSelection: null,
    tableSelected: {}
  }
}
const mutations = {
  SET_graphData (state, val) {
    state.graphData = val
  },
  SET_tableData (state, val) {
    state.tableData = val
  },
  SET_tableSelection (state, val) {
    state.tableSelection = val
  },
  SET_TABLE_SELECTED (state, {sheetName, value}) {
    state.tableSelected[sheetName] = value
  }
}
const actions = {
  async getGraphData ({commit, dispatch, state}) {
    const path = 'http://127.0.0.1:5000/getGraphData'
    var result = await axios.get(path)
    commit('SET_graphData', result['data'])
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
  },
  setTableSelected ({commit, displatch, state}, data) {
    commit('SET_TABLE_SELECTED', data)
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
