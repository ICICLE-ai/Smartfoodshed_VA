<template>
    <v-app>
      <v-app-bar app>
        <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        <v-toolbar-title>ICICLE Visual Analytics V1</v-toolbar-title>
        <!-- <v-spacer></v-spacer> -->
        <div style="width:14%; margin-left:50%">
          <v-select
          v-model="selected_dataset"
          variant="solo"
          hint="Select A Dataset"
          persistent-hint
          :items="['ppod', 'cfs','ci']"
        ></v-select>
        </div>
      </v-app-bar>
    
    <v-navigation-drawer
      v-model="drawer"
      temporary app
      left
      >
      <v-list>
        <template v-for="item in items">
          <v-list-item :key="item.value" @click="ClickEvent(item.value)">
            <v-list-item-icon><v-icon>{{item.icon}}</v-icon></v-list-item-icon>
            <v-list-item-title>{{item.label}}</v-list-item-title>
          </v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-dialog
      v-model="dialog"
      max-width="600px"
      scrollable
    >
      <v-card>
        <v-card-title class="text-h5">
          Select one Cloud data to load 
        </v-card-title>
        <v-card-text>
          <v-data-table
            :headers="tableHeaders"
            :loading="tableLoading"
            :items="tableData"
            :items-per-page="5"
            scrollable
            class="elevation-1"
          ></v-data-table>
        </v-card-text>
      </v-card>
    </v-dialog>
    <dashboard ref="dashboard"/>
    </v-app>
</template>

<script>
import {mapState} from 'vuex'
import Dashboard from '@/views/Dashboard.vue'
import axios from 'axios'
export default {
  data() {
    return {
      selected_dataset: "ppod",
      load: false,
      drawer: false,
      dialog: false,
      items: [
        {
          'value': 'LogIn',
          'label': 'Log In',
          'icon': 'mdi-login'
        },{
          'value': 'SaveData',
          'label': 'Save Data',
          'icon': 'mdi-cloud-upload'
        },{
          'value': 'LoadData',
          'label': 'Load Data',
          'icon': 'mdi-cloud-download'
        }
      ],
      tableHeaders: [],
      tableData: [],
      tableLoading: false
    }
  
  },
  components: {
    Dashboard
  },
  methods: {
    async fetchData(){
      this.$store.dispatch('changeDB',{'database': this.selected_dataset})
    },
    ClickEvent(clickedItem){
      if(clickedItem=="LogIn"){
        // login event
        window.open('https://dev.develop.tapis.io/v3/oauth2/idp')
        // For David: TBA: get user token? and load data?
      }else if(clickedItem=="SaveData"){
        // get the state data
        const savedState = this.$store.state
        //save this data to cloud 
        console.log(savedState)
      }else if(clickedItem=="LoadData"){
        // TODO: get the data object from logged in user: data
        // update the state 
        // var data = {} //to be replaced from cloud data
        // this.$store.state.replaceState(data)
        this.dialog = true
        this.tableLoading = true
        axios.get("https://icfoods.o18s.com/api/storage/json-objects/").then(result=>{
          // this.tableData = result['data']
          this.tableData = result['data'].map(obj => {
            return {
              ...obj,  // Copy all key-value pairs from the original object
              json_data: JSON.stringify(obj['json_data']).slice(0,20)+"..." // Transform the key value to a string
            };
          });
          console.log(this.tableData)
          this.tableHeaders = [{
            text: 'UUID',
            value: 'uuid'
          },{
            text: 'Title',
            value: 'title'
          },{
            text: 'Owner',
            value: 'owner'
          },{
            text: 'Data',
            value: 'json_data'
          }]
        })
        this.tableLoading = false 
      }
    }
  }, 
  created(){
    this.load = true
    // this.fetchData()
  },
  watch: {
    load: function(){
      this.fetchData()
    },
    selected_dataset: function(){
      // window.location.reload();
      // d3.select('#div_graph').html('')
      this.fetchData()
    }
  },
  computed: {
    ...mapState(['BETA_ROUTE', 'DASH_ROUTE']),
    versionPrompt() {
      const currentRoute = this.$route.name
      if (currentRoute == this.DASH_ROUTE.name) {
        return "Try Dashboard Beta"
      }else {
        return "Old Version"
      }
    }
  }
};
</script>

<style>
/* .svg-canvas{
    position: absolute; 
    width: 100%; 
    height: 100%;
    z-index: -1;
  } */
</style>
