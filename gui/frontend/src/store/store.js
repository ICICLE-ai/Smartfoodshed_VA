
import axios from 'axios'
import Vuex from 'vuex'
import Vue from 'vue'
Vue.use(Vuex)
function initialState (){
    return {
        graphData: null,
        tableData: null,
    }
}

const mutations  = {
    SET_graphData(state, val){
        state.graphData = val 
    },
    SET_tableData(state, val){
        state.tableData = val 
    }
}

const actions = {
    async getGraphData({commit, dispatch, state}){
        const path = "http://127.0.0.1:5000/getGraphData" 
        var result = await axios.get(path)
        commit('SET_graphData', result['data'])
    },
    async getTableData({commit, dispatch, state}){
        const path = "http://127.0.0.1:5000/getTableData"
        var result = await axios.get(path)
        console.log(result)
        commit('SET_tableData', result['data'])
    }
}

export const store = new Vuex.Store({
    stric: true, 
    state: initialState,
    mutations: mutations,
    getters: {

    },
    actions: actions
})