<template>
        <v-container id="inspire">
            <div class="tmp">
              <v-tabs v-model="tab"
                  show-arrows
                  next-icon="mdi-arrow-right-bold-box-outline"
                  prev-icon="mdi-arrow-left-bold-box-outline">
                <v-tab
                  v-for="sheetname in sheetNames"
                  :key="sheetname">
                  {{ sheetname }}
                </v-tab>
              </v-tabs>
              <v-tabs-items v-model="tab" ref="tabletabs" style="border: solid 1px rgba(0, 0, 0, 0.54); margin-top: 20px; border-radius: 5px; padding-top:10px">
                <v-tab-item
                v-for="sheetname in sheetNames"
                :key="sheetname">
                <VueTabulator :ref="'tabulator' + sheetname" v-model="currentData['data'][sheetname]['tableData']" :options="currentData['data'][sheetname]['tableInfo']" />            
                </v-tab-item>
              </v-tabs-items>
              <v-btn @click="retrieve">Retrieve</v-btn>
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
      allColumns: null,

    }
  },
  computed: {
    ...mapState(['tableData', 'tableSelection', 'tableSelected', 'tableInteractiveMode', 'interactiveTableData']),
    windowHeight() {
      return (window.innerHeight-350) + "px"
    }
  },
  created(){
  },
  methods: {
    itemSelectedHandler(tab_id){
      var name = 'tabulator'+ this.sheetNames[parseInt(tab_id)]
      var tabulatorIns = this.$refs[name][0].getInstance()
      var selectedData = tabulatorIns.getSelectedData()
      console.log(selectedData);
      this.$store.dispatch('setTableSelected', {action:'add', sheetName: tab_id, value:selectedData})
    },
    retrieve(){
      this.itemSelectedHandler(this.tab)
      this.$store.dispatch("retrieveGraphFromTable")
    },
    filterOnlyCapsText (value, search, item) {
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLowerCase().indexOf(search.toLowerCase()) !== -1
    },
    updateItemKey(){
      this.currentSheet = this.currentData['sheet'][this.tab]
      if (this.currentSheet == null){
        return 
      }
      const sampleData = this.currentData['data'][this.currentSheet]['tableData'][0]; 

      if(sampleData){
        const keys = Object.keys(sampleData)
        // console.log("check =================== here!!!")
        // console.log(sampleData)
        // console.log(this.currentSheet)
        if(keys.includes('relation_id')){
          this.sheetItemKey = 'relation_id'
        }else if(keys.includes('id')){
          this.sheetItemKey = 'id'
        }
      }
    },
    prepareTabulatorData(DATA){ // we transform tableData for the tabulator 
      this.sheetNames = DATA['sheet']
      // console.log(TestData)
      var that = this
      const newData = {}
      for (const [sheetname, sheetdata] of Object.entries(DATA['data'])) {
        // console.log(sheetname, sheetdata)
        var columns = [
            {
              field: 'checkbox',formatter:"rowSelection", titleFormatter:"rowSelection", align:"center", headerSort:false, frozen:true,
              'titleFormatterParams':{
                "rowRange":"active" //only toggle the values of the active filtered rows
            },
            } // adding the tickbox
        ]
        var newColumns = []
        for(let i =0; i<sheetdata['tableInfo'].length; i++){
          // console.log(sheetdata['tableInfo'][i]['value'])
          if (sheetdata['tableInfo'][i]['value'].startsWith('use_case')==false){
            newColumns.push({
            'field': sheetdata['tableInfo'][i]['value'],
            'title': sheetdata['tableInfo'][i]['label'],
            'headerFilter':"input",
            'headerFilterFunc': "keywords",
            
            'headerFilterFuncParams':{matchAll:true}
            })
          }
        }
        // console.log(columns)
        // sorting the columns name/label at the most left, and id at the right most 
        newColumns = newColumns.sort(function(first, second) {
          if(first['field'].toLowerCase().includes('checkbox') || first['field'].toLowerCase().includes('name') ||first['field'].toLowerCase().includes('label') || (second['field'].toLowerCase().includes('id')) || (second['field'].toLowerCase().includes('uri'))){
              return -1
          }else{
              return 1
          }
        });
        newData[sheetname] = {
          'tableInfo': {
            // 'columns': [...columns, ...newColumns],
            'columns': newColumns,
            'height': parseInt(that.windowHeight.replace('px',''))+200,
            'movableColumns': true,
            'movableRows': true,
            'selectable': true,
          }, 
          'tableData': sheetdata['tableData']
        }
      }
      this.currentData = {
        'sheet': DATA['sheet'],
        'data': newData
      }
      console.log('finishing updateing data,', this.currentData)
    },
    tableUpdate(DATA){ // once the table got updated, we need to do a sequence of things
      // check if it is in the tableInteractiveMode (which means table got updated from graph)
      // console.log('updating.. data... table...based on the data', DATA)
      if(DATA['sheet'].length>0){
        this.prepareTabulatorData(DATA)
        if(this.tab==null){
          this.tab=0
        }
        console.log()
        this.updateItemKey()
      }else{
        alert('Nothing retrieved from table!')
      }
    }
  },
  watch:{
    tableData () { // tableData is changed, we need to call tableUpdate() to update a sequence of things 
      if(!this.tableInteractiveMode){
        this.tableUpdate(this.tableData)
      }
    },
    tableInteractiveMode(){ // if the tableInteractiveMode changes, 
      if(!this.tableInteractiveMode){
        this.tableUpdate(this.tableData)
      }
    },
    interactiveTableData(){ // interactive Table Data, updated from the graph    
      if(this.tableInteractiveMode){
        this.tableUpdate(this.interactiveTableData)
      }
    },
    tab(newVal, oldVal) { 
      // console.log('tab changed', newVal, oldVal)
      if (this.currentData != null) {
        this.updateItemKey()
      }
      if(oldVal!=null){
        this.itemSelectedHandler(oldVal) //once we change a tab, get all selected item from previous sheet 
      }
      
      // console.log(this.sheetItemKey)
    }, 
  }, 
  
}

</script>
<style>
#inspire{
  height: 100%;
}
.tabulator .tabulator-header .tabulator-col.tabulator-sortable .tabulator-col-title{
  color: #1976d2;
  font-weight: normal;
  font-size:0.84rem
}
.tabulator .tabulator-header{
  border-bottom:3px solid #1976d2 !important;
  color: #1976d2
}
.tabulator-row .tabulator-cell {
  font-size: 0.84rem;
}
.tabulator-row .tabulator-cell:first-child{
  border-left: 10px solid #1976d2;
}
.tabulator .tabulator-header .tabulator-col .tabulator-header-filter{
  font-size: 0.84rem
}
</style>