<template>
  <div>
    <v-hover v-slot="{ hover }">
      <v-card
        :elevation="hover ? 12 : 5"
        class="card-tabular"
        :draggable="draggable"
        @dragstart="dragStart"
        outlined
        :id="componentId"
        ref="cardComp"
        @contextmenu="rightClickMenuShow"
        @dblclick="printCorpus"
        :style="{
          top: marginTop + 'px',
          left: marginLeft + 'px',
          width: `${width}px`,
          height: `${height}px`,
          position: 'absolute',
        }"
      > 
         
        <template>
            <v-card-text v-if="!dataStatus" class="card-name">
                No Table Data
            </v-card-text>
            <div v-if="dataStatus">
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
                        :height="`${height - 50 - 70 - 150}px`"
                        v-model="selected_rows"
                        :loading="loadingStatus"
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
                              label="Search (UPPER CASE ONLY)"
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
        </template>

        <div class="resizer resizer-r" @mousedown="mouseDownHandler"></div>
        <div class="resizer resizer-b" @mousedown="mouseDownHandler"></div>
      </v-card>
    </v-hover>
    <!-- <v-menu
      v-model="showRightClickMenu"
      :position-x="rightMenuX"
      :position-y="rightMenuY"
      absolute
      offset-y
    >
      <RightClickMenu
        :vue="this"
        :container="container"
        :itemProps="itemProps"
        store="documents"
      />
    </v-menu> -->
  </div>
</template>

<script>
import { mapState } from "vuex";
// import RightClickMenu from "@/components/RightClickMenu";
// import InoutputBtns from "@/components/InoutputBtns";
export default {
  data() {
    return {
      initialX: undefined,
      initialY: undefined,
      dataStatus: false,
      resizeX: undefined,
      resizeY: undefined,
      // draggable: true,
      width: 500,
      height: 600,
      resizeWidth: 0, //
      resizeHeight: 0,
      marginTop: 0,
      marginLeft: 0,
      topMargin: window.innerHeight / 2,
      leftMargin: window.innerWidth / 2,
      resizingStatus: false,
      ff:false, 

    //   showRightClickMenu: false,
      rightMenuX: 0,
      rightMenuY: 0,
      loadingStatus: undefined,
      componentId: "tabular-0",
      // for right click menu
      items: [{ title: "Remove node" }],

      container: ".documents-components-list",

      selected: [],
     
      sheets: [], 
      
      currentDataBase: [],
      answerBasedRetrieval: {},
      flag: false,
      tableItemKey: "",
      //-----
      search: "",
      calories: '', 
      desserts: [],
      headers: [],
      
      selected_rows:[],
      singleSelect: false,
      sheetNames: [],
      tab: null,
      sheetItemKey: null, 
      currentSheet: null, 
      currentData: null,
    };
  },
  methods: {
    dragStart(e) {
      const el = document.querySelector(`#${e.target.id}`);
      const initialLeft = parseInt(el.style.left.split("px")[0]) - e.clientX;
      const initialTop = parseInt(el.style.top.split("px")[0]) - e.clientY;
      e.dataTransfer.setData("item-id", e.target.id);
      e.dataTransfer.setData("initialLeft", initialLeft);
      e.dataTransfer.setData("initialTop", initialTop);
      this.$store.dispatch("changeCurrentDraggingVM", this);
    },

    mouseDownHandler(e) {
      // this.$store.dispatch('changeResizerStatus', true);
      this.resizeX = e.clientX;
      this.resizeY = e.clientY;
      document.addEventListener("mousemove", this.mouseMoveHandler);
      document.addEventListener("mouseup", this.mouseUpHandler);
      this.resizingStatus = true;
    },

    mouseMoveHandler(e) {
      const dx = e.clientX - this.resizeX;
      const dy = e.clientY - this.resizeY;
      this.width = this.resizeWidth + dx;
      this.height = this.resizeHeight + dy;
    },

    mouseUpHandler(e) {
      this.resizeWidth = this.width;
      this.resizeHeight = this.height;
      document.removeEventListener("mousemove", this.mouseMoveHandler);
      document.removeEventListener("mouseup", this.mouseUpHandler);
      // this.$store.dispatch('changeResizerStatus', false)
      this.resizingStatus = false;
    },

    rightClickMenuShow(e) {
      e.preventDefault();
      this.showRightClickMenu = true;
      this.rightMenuX = e.clientX;
      this.rightMenuY = e.clientY;
    },

    printCorpus() {
      console.log(this.itemProps);
    },

    toggleSheet(sheetName){
      if (this.currentSheet != sheetName) {
        this.currentSheet = sheetName;
        this.sheetDataUpdate(this.currentSheet);
      }
    },

    sheetDataUpdate(sheetName){
      const val = this.itemProps.inputData; 
      const tableValue = val["data"][sheetName];
      this.headers = []
     
      if(Object.keys(tableValue).length > 0){
        for (let key of Object.keys(tableValue[0])) {
          this.headers.push({
            text: key.charAt(0).toUpperCase() + key.slice(1), //
            value: key,
          }); 
        }
        this.tableItemKey = this.headers[0]["value"];
        this.currentDataBase = Object.values(tableValue);
        this.desserts = Object.values(tableValue);
      }
    }, 
    filterOnlyCapsText (value, search, item) {
      console.log(value, search, item)
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().indexOf(search) !== -1
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
  
  created() {
    // Initialize initial position
    this.$store.dispatch('getTableData')
    this.marginTop = this.topMargin - this.height / 2;
    this.marginLeft = this.leftMargin - this.width / 2;
    this.resizeWidth = this.width;
    this.resizeHeight = this.height;
  },

  computed: {
    ...mapState(['tableData', 'tableSelection', 'tableSelected', 'tableInteractiveMode', 'interactiveTableData']),

    // Determine Whether the component is draggable
    // Not allowed when resizing and drawling link
    draggable() {
      return !(this.resizingStatus);
    },
  },

  components: {
  },

  watch: {

    tableData () {
      if (!this.tableInteractiveMode) {
        this.dataStatus = true
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
        this.dataStatus = true
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
    // "itemProps.inputData": function (val, oldVal) {
    
    //   console.log("newVal, oldVal");
    //   if (val) {
    //     this.loadingStatus = true;
    //     this.dataStatus = val.tableNames;
    //     this.headers = [];

    //     const tableNames = val['tableNames']; 
    //     tableNames.forEach(tablename => {
    //       this.sheets.push({
    //         name: tablename,
    //         active: true,
    //       })
    //     })
        
    //     this.currentSheet = tableNames[0];

    //     this.sheetDataUpdate(this.currentSheet);

    //     this.loadingStatus = false;
    //   } else {
    //     this.loadingStatus = false;
    //     this.dataStatus = undefined;
    //     this.currentDataBase = undefined;
    //     this.desserts = undefined;
    //   }
    // },

    dataStatus: function(val, oldVal) {
        if (val) {
        const resizerBElelemt = document.querySelector("#" + this.componentId).querySelector(".resizer-b"); 
        const heightOfSheet = 25;
        resizerBElelemt.style.bottom = (-heightOfSheet - 12) + "px"; 
        }
    }, 
    marginTop(newVal) {
       console.log(newVal);
    }
   
  },
};
</script>

<style scoped>
.card-name {
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  height: 100%;
}

/* .card-actions{
    position: absolute;
    transform: translate(300px, -150px);
    padding: 0;
  } */

.resizer {
  position: absolute;
}

.resizer-r {
  cursor: col-resize;
  height: 100%;
  right: -1%;
  top: 0;
  width: 5px;
}

/* Placed at the bottom side */
.resizer-b {
  bottom: 0;
  cursor: row-resize;
  height: 5px;
  left: 0;
  width: 100%;
}

.v-data-footer {
  height: 50px !important;
}

.sheetname{
  margin-top: 10px;
  height: 20px;
}
</style>                                                                   