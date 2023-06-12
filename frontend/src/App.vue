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
      v-model="dialog_load"
      max-width="600px"
      scrollable
    >
      <v-card>
        <v-card-title class="text-h5">
          Select one Cloud data to load 
        </v-card-title>
        <v-card-text>
          <v-data-table
          @click:row="selectCloudData"

            show-select
            persistent
            single-select
            item-key="uuid"
            :headers="tableHeaders"
            :loading="tableLoading"
            loading-text="Loading... Please wait"
            :items="tableData"
            :items-per-page="5"
            scrollable
            class="elevation-1"
          ></v-data-table>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialog_save"
      max-width="600px"
      persistent 
      scrollable>
      <v-card>
        <v-card-title>Dataset Profile</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="Dataset Title"
                  required
                  v-model="input_data_title"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  label="Owner Name"
                  v-model="input_data_owner"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="dialog_save = false"
          >
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
            text
            @click="saveCloudData"
            :loading = "dialog_save_loading"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="show_alert"
    max-width="300px"
    >
      <v-alert
        :color="alertInfo.alert_color"
        variant="tonal"
        closable
      > 
        {{alertInfo.alert_text }}
    </v-alert>
    </v-dialog>
    
    <dashboard ref="dashboard"/>
    </v-app>
</template>

<script>
import {mapState} from 'vuex'
import Dashboard from '@/views/Dashboard.vue'
import axios from 'axios'
import { getItemIndex } from './utils/storehelp';
export default {
  data() {
    return {
      selected_dataset: "ppod",
      load: false,
      drawer: false,
      dialog_load: false,
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
      tableLoading: false,

      dialog_save: false,  // save data dialog
      input_data_title: "", // save data form 
      input_data_owner: "", // save data form 
      dialog_save_loading: false, 
      alertInfo:{
        alert_color: 'success',
        alert_title: 'Successfully saved!',
        alert_text: 'The uuid for saved data is:'
      },
      show_alert : false
    }
  
  },
  components: {
    Dashboard
  },
  methods: {
    saveCloudData(){
      const savedState = this.$store.state
      var data2save = {
        "title": this.input_data_title,
        "owner": this.input_data_owner, // TODO : to be dynamic 
        "json_data": savedState
      }
      this.dialog_save_loading = true 
      var path = "https://icfoods.o18s.com/api/storage/json-object/create/"
      axios.post(path, data2save)
      .then(response => {
        console.log(response)
        this.alertInfo = {
          alert_color: "success",
          alert_title: "Successfully saved!",
          alert_text: "The uuid for saved data is: "+ response.data.uuid
        }
        // console.log(this.alertInfo)
        this.dialog_save_loading = false
        this.dialog_save = false
        this.show_alert = true
      })
      .catch(error => {
        this.alertInfo = {
          alert_color: "error",
          alert_title: "Error occured!",
          alert_text: error
        }
        this.dialog_save_loading = false
        this.dialog_save = false
        this.show_alert = true
      })
    },
    selectCloudData(item, slot){
      slot.select(!slot.isSelected)// click anywhere in the row will automatically select the checkbox 
      // console.log('test', item, item['uuid'])
      // fetch the data 
      axios.get("https://icfoods.o18s.com/api/storage/json-object/"+item['uuid']+"/").then(result=>{
        this.$store.state.replaceState(result['data'])
      })
    },
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
        this.dialog_save = true
      }else if(clickedItem=="LoadData"){
        // TODO: get the data object from logged in user: data
        // update the state 
        // var data = {} //to be replaced from cloud data
        // this.$store.state.replaceState(data)
        this.dialog_load = true
        this.tableLoading = true
        axios.get("https://icfoods.o18s.com/api/storage/json-objects/").then(result=>{
          // this.tableData = result['data']
          this.tableData = result['data'].map(obj => {
            return {
              ...obj,  // Copy all key-value pairs from the original object
              json_data: JSON.stringify(obj['json_data']).slice(0,20)+"..." // Transform the key value to a string
            };
          });
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
          this.tableLoading = false 
        })
        
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
