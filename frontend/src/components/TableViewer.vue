<template>
        <v-container id="inspire">
            <div class="tmp">
              <v-tabs v-model="tab">
                <v-tab
                  v-for="sheetname in sheetNames"
                  :key="sheetname"
                >
                  {{ sheetname }}
                </v-tab>
              </v-tabs>
             <v-tabs-items v-model="tab" ref="tabletabs">
                <v-tab-item
                  v-for="sheetname in sheetNames"
                  :key="sheetname"
                >
                   <v-data-table
                      fixed-header
                        :height="windowHeight"
                        v-model="selected_rows"
                        show-select
                        :headers="convert(currentData['data'][sheetname]['tableInfo'])"
                        :items="currentData['data'][sheetname]['tableData']"
                        :item-key="sheetItemKey"
                        :single-select="singleSelect"
                        class="elevation-1"
                        :search="search"
                        :custom-filter="filterOnlyCapsText"
                        @item-selected="itemSelectedHandler"
                        @toggle-select-all="selectAllHandler"
                    >
                        <template v-slot:top>
                          <v-text-field
                              v-model="search"
                              label="Search"
                              class="mx-4"
                              style="margin-top: 3px"
                          ></v-text-field>
                        </template>
                        <template v-slot:footer>
                          <v-container>
                            <v-row
                              justify="space-between"
                            >
                              <v-col cols="3">
                                <v-text-field
                                  v-model="calories"
                                  type="number"
                                  label="Less than"  
                                  style="width: 80px"

                              ></v-text-field>
                              </v-col>
                              <v-col cols="3" style="margin-top:20px">
                                 <v-btn @click="retrieveGraphFromTableHandler">
                                  Retrieve
                                </v-btn>
                              </v-col>
                            </v-row>
                          </v-container>
                        </template>
                    </v-data-table>
                </v-tab-item>
              </v-tabs-items>
           
            </div>
        </v-container> 
</template>

<script>
import {mapState} from 'vuex'
export default{
    data () {
    return {
      search: '',
      calories: '',
      desserts: [],
      headers:[],

      selected_rows:[],
      singleSelect: false,
      sheetNames: [],
      tab: null,
      sheetItemKey: null, 
      currentSheet: null, 
      currentData: null, 
    }
  },
  computed: {
    ...mapState(['tableData', 'tableSelection', 'tableSelected', 'tableInteractiveMode', 'interactiveTableData']),
    windowHeight() {
      return (window.innerHeight-350) + "px"
    }
  },
  created(){
    this.$store.dispatch('getTableData')
  },
  methods: {
    filterOnlyCapsText (value, search, item) {
      // console.log(value, search, item)
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLowerCase().indexOf(search.toLowerCase()) !== -1
    },
    convert(raw){
      // vuetify need the text + value, not label+value 
      let newOutput = []
      raw.forEach(d=>{
        let temp = {
          text: d['label'],
          value: d['value'],
        }
        newOutput.push(temp)
      })
      return newOutput
    }, 
    itemSelectedHandler({item, value}){
      
      if (value) {
        this.$store.dispatch('setTableSelected', {action: 'add', sheetName: this.currentSheet, value: [item]})
      } else {
        this.$store.dispatch('setTableSelected', {action: 'remove', sheetName: this.currentSheet, value: [item]})
      }
    }, 
    retrieveGraphFromTableHandler(){ 
      this.$store.dispatch("retrieveGraphFromTable")
    }, 
    selectAllHandler({items, value}){
      console.log(items, value)
      if (value) {
        this.$store.dispatch('setTableSelected', {action: 'add', sheetName: this.currentSheet, value: items})
      } else {
        this.$store.dispatch('setTableSelected', {action: 'remove', sheetName: this.currentSheet, value: items})
      }
    },
    updateItemKey(){
      this.currentSheet = this.currentData['sheet'][this.tab]
      if (this.currentSheet == null){
        return 
      }
      const sampleData = this.currentData['data'][this.currentSheet]['tableData'][0]; 

      if(sampleData){
        const keys = Object.keys(sampleData)
        console.log("check =================== here!!!")
        console.log(sampleData)
        console.log(this.currentSheet)
        if(keys.includes('relation_id')){
          this.sheetItemKey = 'relation_id'
        }else if(keys.includes('id')){
          this.sheetItemKey = 'id'
        }
      }
    }
  },
  watch:{
    tableData () {
      if (!this.tableInteractiveMode) {
        this.sheetNames = this.tableData['sheet']
        console.log("check here!!!")
        console.log(this.tableData)
        this.currentData = this.tableData
        if(this.tab==null){
          this.tab = 0
        } 
        this.updateItemKey()
      }
    },
    tableInteractiveMode(){
      if(!this.tableInteractiveMode){
        this.currentData = this.tableData
        this.sheetNames = this.currentData['sheet'] 
        if(this.tab==null){
              this.tab = 0
        } 
        this.updateItemKey()
        this.selected_rows = []
      }   
    },
    interactiveTableData(){
      console.log(this.interactiveTableData)
      if(this.tableInteractiveMode){
        if(this.interactiveTableData['sheet'].length > 0){
          this.currentData = this.interactiveTableData
          this.sheetNames = this.currentData['sheet']
          // console.log("**********************")
          // console.log(this.interactiveTableData)
          if(this.tab==null){
              this.tab = 0
            } 
          this.updateItemKey()
          this.selected_rows = []
        }else{
          alert("Nothing retrieved from table!")
          this.selected_rows = []
        }
      }
    },
    tab() {
      // tab id
      // const tabId = this.tab
      console.log(this.currentData)
      if (this.currentData != null) {
        this.updateItemKey()
      }
      console.log(this.sheetItemKey)
    }, 
  }, 
  
}

</script>
<style>
/* .v-input__slot{
  width: 100px;
} */

#inspire{
  height: 100%;
}
</style>