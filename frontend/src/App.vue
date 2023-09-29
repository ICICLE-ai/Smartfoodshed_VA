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
          :items="['ppod', 'cfs']"
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
          <v-list-item :key="item.value" v-if="checkVisible(item.label)" @click="ClickEvent(item.value)">
            <v-list-item-icon><v-icon>{{item.icon}}</v-icon></v-list-item-icon>
            <v-list-item-title>{{check(item.label)}}</v-list-item-title>
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
          Select a Cloud Data Source to Load 
          <v-btn @click="loadData" :loading = "dialog_load_loading">Load</v-btn>
        </v-card-title>
        <v-card-text>
          <v-data-table
          @click:row="rowClick"
            single-select
            item-key="uuid"
            :headers="tableHeaders"
            :loading="tableLoading"
            loading-text="Loading... Please wait"
            :items="tableData"
            :items-per-page="5"
            scrollable
            class="elevation-1"
          >
        </v-data-table>
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
// import TEST from '../public/testing.json'
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
          'value': 'LogOut',
          'label': 'Log Out',
          'icon': 'mdi-logout'
        },{
          'value': 'SaveData',
          'label': 'Save Data',
          'icon': 'mdi-cloud-upload'
        },{
          'value': 'LoadData',
          'label': 'Load Data',
          'icon': 'mdi-cloud-download'
        },
      ],
      tableHeaders: [],
      tableData: [],
      tableLoading: false,

      dialog_save: false,  // save data dialog
      input_data_title: "", // save data form 
      dialog_save_loading: false, 
      alertInfo:{
        alert_color: 'success',
        alert_title: 'Successfully saved!',
        alert_text: 'The uuid for saved data is:'
      },
      show_alert : false,

      selectedRow: undefined,
      dialog_load_loading: false
    }
  
  },
  components: {
    Dashboard
  },
  methods: {
    checkVisible(ele){
      if(ele=="Log Out" || ele=="Save Data"){
        if(this.getCookieByName('token')==null){ //not logged in
          return false
        }else{
          return true 
        }
      }else{
        return true
      }
    },
    check(ele){
      if(ele=="Log In"){
        if(this.getCookieByName('token')==null){ //not logged in
          return "Log In"
        }else{
          return this.getCookieByName('username')
        }
      }else{
        return ele
      }
    },
    rowClick: function (item, row) {      
      row.select(true);
      this.selectedRow = item
    },
    // click save to save data to cloud 
    getCookieByName(name) {
      const cookies = document.cookie.split(';'); // Split cookies by semicolon
      for (const cookie of cookies) {
        const [cookieName, cookieValue] = cookie.trim().split('=');
        if (cookieName === name) {
          return decodeURIComponent(cookieValue); // Return decoded value
        }
      }
      return null; // Return null if cookie not found
    },
    // Delete cookie
    deleteCookieByName(name) {
      //document.cookie = name +'=; Path=/; Domain=localhost; Expires=' + new Date(0).toUTCString() + ';'; //For local use only 
      document.cookie = name +'=; Path=/; Domain=.pods.icicle.tapis.io; Expires=' + new Date(0).toUTCString() + ';';
    },
    saveCloudData(){
      const savedState = this.$store.state
     
      // console.log('tosave', data2save)
      // alert(document.cookie);
      var data2save = {
        "title": this.input_data_title,
        "owner": this.getCookieByName('username'), // TODO : to be dynamic 
        "json_data": savedState,
      }

      const config = {
        headers:{
          authorization: `Token ${this.getCookieByName('token')}`,

        }
      };
      // axios.post(path,data2save,config)
      // this.dialog_save_loading = true 
      var path = "https://icfoods.o18s.com/api/storage/json-object/create/"
      // var path = "https://icfoods.o18s.com/api/tapis/protected/"
      axios.post(path, data2save, config)
      // axios.get(path, config)
      .then(response => {
        this.alertInfo = {
          alert_color: "success",
          alert_title: "Successfully saved!",
          alert_text: "The uuid for saved data is: "+ response.data.uuid
        }
        // console.log(this.alertInfo)
        this.dialog_save_loading = false // end spinning
        this.dialog_save = false // hide the dialog 
        this.show_alert = true // show notification 
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
    // click load to load data from cloud 
    loadData(){
      // slot.select(!slot.isSelected)// click anywhere in the row will automatically select the checkbox 
      // fetch the data 
      this.dialog_load_loading = true
      axios.get("https://icfoods.o18s.com/api/storage/json-object/"+this.selectedRow['uuid']+"/").then(result=>{
        var temp = result['data']['json_data']
        temp['resetMode'] = true
        this.$store.dispatch('resetState',temp)
        this.dialog_load_loading = false
        this.dialog_load = false
      })
    },
    // loadDataTesting(){
    //   // console.log(TEST)
    //   TEST['json_data']['resetMode'] = true 
    //   console.log(TEST)
    //   this.$store.dispatch('resetState',TEST['json_data'])
    //   this.dialog_load_loading = false
    //   this.dialog_load = false
    // },
    //change database 
    async fetchData(){
      this.$store.dispatch('changeDB',{'database': this.selected_dataset})
    },
    // click the left navigation panel 
    async ClickEvent(clickedItem){
      if(clickedItem=="LogIn"){
        // login event
        if(this.getCookieByName('token')==null){
          await this.$store.dispatch('logIn')
          this.item[1]['visible']=true //Shows logout
          this.items[2]['visible']=true //Shows to save data
        }
      }else if(clickedItem=="SaveData"){
        // get the state data
        this.dialog_save = true
      }
      else if(clickedItem=="LoadData"){
        this.dialog_load = true
        this.tableLoading = true
        // this.loadDataTesting()
        const config = {
        headers:{
          AUTHORIZATION: `Token ${this.getCookieByName('token')}`,

        }
      }
        axios.get("https://icfoods.o18s.com/api/storage/json-objects/", config).then(result=>{
          this.tableData = result['data'].map(obj => {
            return {
              ...obj,  // Copy all key-value pairs from the original object
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
          }]
          this.tableLoading = false 
        })
      }
      else if(clickedItem=="LogOut"){
          // For Carlos 
          this.deleteCookieByName("username");
          this.deleteCookieByName("token");
          this.items[1]['visible']=false // hide the log out button
          this.items[2]['visible']=false // hide the save data button
      }
    }
  }, 
  created(){
    this.load = true
  },
  watch: {
    
    selectedRow: function(){
      console.log('select changes')
    },
    load: function(){
      this.fetchData()
    },
    selected_dataset: function(){
      // window.location.reload();
      // d3.select('#div_graph').html('')
      this.fetchData()
    },
    loginRedirect: function(){
      // alert(this.loginRedirect)
      if(this.loginRedirect!="/"){
        window.location.href = this.loginRedirect;
      }
    }
  },
  computed: {
    ...mapState(['BETA_ROUTE', 'DASH_ROUTE', 'loginRedirect']),
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
tr.v-data-table__selected {
  background: #7d92f5 !important;
}
/* .svg-canvas{
    position: absolute; 
    width: 100%; 
    height: 100%;
    z-index: -1;
  } */
</style>
