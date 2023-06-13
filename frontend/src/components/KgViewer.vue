<template>
    <div class="fullHeight" style="position:relative">
        
        <div
          class="graph-btn-container"
        >
        <v-container>
          <v-row no-gutters
            justify='space-between'
          >
          <v-col
          key="0"
          sm="4"
          >
          <v-card-subtitle>Graph Control Panel</v-card-subtitle>
          </v-col>
          <v-col
            key="1"
            sm="5"
            cols="12"
            style="border:1px #BDBDBD solid; border-radius:3px"
            >
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn 
                  class="ma-2 menu-btn"
                  icon
                  text
                  @click="resetGraphTableHandler"
                >
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-refresh
                  </v-icon>
                </v-btn>
              </template>
              <span>Reset</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn 
                  class="ma-2 menu-btn"
                  icon
                  text
                  :color="zoomPanColor"
                  @click="zoomPanToggleHandler"
                >
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-arrow-expand-all
                  </v-icon>
                </v-btn>
              </template>
              <span>ZOOM</span>
            </v-tooltip>

            
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn 
                  class="ma-2 menu-btn"
                  icon
                  text
                  :color="lassoColor"
                  @click="lassoToggleHandler"
                >
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-lasso
                  </v-icon>
                </v-btn>
              </template>
              <span>LASSO</span>
            </v-tooltip>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn 
                  class="ma-2 menu-btn"
                  icon
                  text
                  @click="showOverview = !showOverview"
                >
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-chart-bar
                  </v-icon>
                </v-btn>
              </template>
              <span>Dataset Overview</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn 
                  class="ma-2 menu-btn"
                  icon
                  text
                  @click="showMaxRetrieve = !showMaxRetrieve"
                >
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-soundbar
                  </v-icon>
                </v-btn>
              </template>
              <span>Maximum Retrieval #</span>
            </v-tooltip>
            
            <v-menu
              v-model="menu"
              :close-on-content-click="false"
              :nudge-width="200"
              offset-x
            > 
              <template v-slot:activator="{ on: menu, attrs }">
              <v-tooltip bottom>
                <template v-slot:activator="{ on: tooltip}">
                  <v-btn 
                    class="ma-2 menu-btn"
                    icon
                    text 
                  >
                    <v-icon
                      v-bind="attrs"
                      v-on="{ ...tooltip, ...menu }"
                      :style="{color: selectedColor?selectedColor.hex:'green'}"
                    >
                      mdi-palette
                    </v-icon>
                  </v-btn>
                </template>
                <span>Color Picker</span>
              </v-tooltip>
              </template>
              <v-card>
                <v-color-picker
                  class="ma-2"
                  show-swatches
                  swatches-max-height="300px"
                  v-model = "selectedColor"
                ></v-color-picker>
              </v-card>
            </v-menu>
            
            <!-- <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn 
                  class="ma-2 menu-btn"
                  icon
                  text
                  @click="showResThre = !showResThre"
                >
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-soundbar
                  </v-icon>
                </v-btn>
              </template>
              <span>Resilience Threshold #</span>
            </v-tooltip> -->
            

            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn 
                  class="ma-2 menu-btn"
                  icon
                  text
                  @click="showStrength = !showStrength"
                >
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-soundbar
                  </v-icon>
                </v-btn>
              </template>
              <span>Graph Layout Strength(negative for repulsion; positive for attraction)</span>
            </v-tooltip>
            
            <v-slider
              v-model="user_defined_thre"
              :thumb-size="24"
              @click="changeThreshold"
              max="1000"
              thumb-label="always"
              v-show="showMaxRetrieve"
            ></v-slider>

            <!-- <v-slider
              v-model="resilience_thre"
              :thumb-size="24"
              min="0"
              step="0.00001"
              :max = max_resilience
              thumb-label="always"
              v-show="showResThre"
            ></v-slider> -->
            
            <v-slider
              v-model="user_defined_strength"
              :step="1"
              label="Strength"
              min="-100"
              max="500"
              hide-details
              class="ma-4"
              v-show="showStrength"
            >
              <template v-slot:append>
                <v-text-field
                  v-model="user_defined_strength"
                  type="number"
                  style="width: 80px"
                  density="compact"
                  hide-details
                  variant="outlined"
                ></v-text-field>
              </template>
            </v-slider>
          </v-col>
        </v-row>
        </v-container>
        </div>
        <node-rel-overview
          v-show="showOverview"
          :graphOverview="graphOverview"
        />
      
        <div id="div_graph" class="fullHeight" :style="{'height': HEIGHT}" style="border:1px #BDBDBD solid; border-radius:3px"></div>  
  
         
        <v-overlay :value="loading_value">
        <v-progress-circular
          indeterminate
          size="64"
        ></v-progress-circular>
      </v-overlay>
    </div>
</template>

<script>
import * as Neo4jd3 from '../js/Neo4D3_v2'
import * as d3Lasso from 'd3-lasso'
import * as d3 from 'd3'
import * as KGutils from '@/utils/KGutils.js'
import {mapState} from 'vuex'
import * as d3tip from '@/utils/d3-tip'
import NodeRelOverview from '@/components/NodeRelOverview'
export default{
  components: {
    NodeRelOverview
  },
  data () {
    return {
      selectedEntities: [], 
      selectedRelations: [],
      currentEntities: [], 
      currentRelations: [],
      lassoColor: "grey", 
      zoomPanColor: "green", 
      lassoStatus: false,
      zoomPanStatus: true, 
      lasso: null, 
      zoom: null, 
      loading_value:false,
      tip: null,
      user_defined_thre: 5,// user defined threshold to show how many nodes we want to see if we expand one node 
      neo4jd3 : null,
      brushed: {"entity_type": [], "relationship_type": []},
      showOverview:false, 
      showMaxRetrieve:false,
      fav: true,
      menu: false,
      message: false,
      hints: true,
      selectedColor: null, 
      showResThre: false, // resilience threshold bar 
      resilience_thre: 0,  // selected threshold of resilience 
      // min_resilience: 0,
      max_resilience: 1, // maximum value of the scroll bar for resilience threshold 

      showStrength: false,
      user_defined_strength: 100
    }
  },
  created () {
    window['d3'] = d3
    this.tip = d3tip()
            .attr('class', 'd3-tip')
            .offset([-10, 80])
            .html(function(d) {
              return "<strong>Relation: </strong>" + d + "<br></span>";
    })
  },
  methods: {
    changeThreshold(){
      // change user define threshold for how many nodes we want to expand 
      this.$store.dispatch('setExpandTh', this.user_defined_thre)
    },
    saveGraphDrawing(){
      this.$store.dispatch('updateNeo4jDrawData', this.neo4jd3.saveData())
    },
    drawNeo4jd3 () {
      var that = this
      d3.selectAll(".d3-tip").remove()      
      if(this.neo4jd3 == null){
        var neo4jd3 = Neo4jd3.default('#div_graph', {
          neo4jData: this.graphData,
          nodeRadius: 30,
          infoPanel: true,
          strength: this.user_defined_strength,
          onNodeDoubleClick: function (node) {
          },
          onNodeMouseEnter: function (node) {
            that.hover_node = node
          },
          zoomFit: true,
          onNodeClick: function (node,idx) {
            if (node.showBtnPanel == true) {
              d3.select(`#node-${node.id}`).selectAll('.circle-button').remove()
              node.showBtnPanel = false
              return
            }
            node.showBtnPanel = true 
            var data = { b: {action: "remove", value: 10, pos:0} } // only two operations 
            if(that.relationStatusReady==false){
              // render the loading panel 
              console.log('nononono')
              //
            }else{
              if(that.relationStatusReady=="fromMap"){
              var relation_data = node['relationship_types']
            }
            else{
              var filtered_relation_type_data = that.relationTypeData['results'][0]['data'][0]['graph']['nodes'].filter(d => d.id == node.id)
              var relation_data = filtered_relation_type_data[0]['relationship_types']
              // get the sum of all rel counts 
            }
            const sumValues = obj => Object.values(obj).reduce((a, b) => a + b);
              const total_c  = sumValues(relation_data)
              // generate the dount data
              for (const [key, value] of Object.entries(relation_data)) {
                data[key] = {action: key, value: (value/total_c)*30}
              }
            } 
            // sorting 
            
            let this_g = d3.select(`#node-${node.id}`)

            // let append_g = this_g.append('g').attr("transform", "translate(" + node['x'] + "," + node['y'] + ")");
            let append_g = this_g

              // Compute the position of each group on the pie:
            var pie = d3.pie()
              .sort(null) //avoiding to sort the pie, make sure the remove button in the same position 
              .value(function(d) {return d.value.value; })
            var data_ready = pie(d3.entries(data))
              // removal / expand operations 
            var operation_buttons_g = append_g.selectAll('whatever')
              .data(data_ready)
              .enter()
            
            var operation_buttons = operation_buttons_g.append('path')
              .attr('d', d3.arc()
                .innerRadius(30)         // This is the size of the donut hole
                .outerRadius(50)
              )
              .attr("class", "circle-button")
              .attr('fill', function(d,i){ 
                if(i==0){
                  return "#BB6464"
                }else{
                  return "#94B49F"
                } 
              })
              // .attr("stroke", "black")
              .style("stroke-width", "2px")
              .style("stroke", "white")
              .style("opacity", 0.7)
              .style('cursor','pointer')
              .attr('title','test')

            var hide_icon = operation_buttons_g.append('path') 
              .attr('d', 'M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M7,13H17V11H7')
              .attr("transform", 'translate(20, -35) scale(0.7)')
              .attr("class", "circle-button")
            
            

            d3.select('svg').call(that.tip)
              // hovering effect 
            operation_buttons.on('mouseover', function(p){
                d3.select(this).style('opacity',1)
                let rel = p['data']['value']['action']
                console.log(rel)
                that.tip.show(rel);
              })
              .on('mouseout',function(p){
                d3.select(this).style('opacity',0.7)
                let rel = p['data']['value']['action']
                that.tip.hide(rel);
              })
              .on('click', function(d,i){
                let clicked_node_id = node['id']
                const action = d.data.value.action 
                // console.log(d)
                that.tip.hide(d.data.value.action)
                if (action == "remove"){
                  // tip.hide(d.data.value.action)
                  that.$store.dispatch("node_remove", {node_id: clicked_node_id})
                }else {
                  // console.log(d.data.value.action)
                  that.$store.dispatch("node_expand", {node_id: clicked_node_id, relation: d.data.key})
                }
              })
          }
      })
        this.neo4jd3 = neo4jd3
      }else{
        console.log('neo4jd3 is not null', this.user_defined_strength)
        // this.neo4jd3.updateSimulation(this.user_defined_strength)
        this.neo4jd3.updateWithNeo4jData(this.graphData, this.user_defined_strength)
      }

      window.neo4jd3 = this.neo4jd3
      window.graph = this.graphData
      if (that.lassoStatus) {
        that.disableZoom()
        that.enableLasso()
      } else {
        that.disableLasso() 
        that.enableZoomPan()
      }
      that.saveGraphDrawing()
      // that.enableLasso()
      
    },
    resetGraphTableHandler(){
      this.$store.dispatch("resetTableGraph")
    },
    toggleZoomPanLasso(){
      this.zoomPanStatus = !this.zoomPanStatus 
      this.lassoStatus = !this.lassoStatus
      this.zoomPanColor = this.zoomPanStatus?"green":"grey"
      this.lassoColor = this.lassoStatus?"green":"grey"
    }, 
    zoomPanToggleHandler() {
      if (!this.zoomPanStatus) {
        this.toggleZoomPanLasso() 
        this.disableLasso()
        this.enableZoomPan()
      }
      
    }, 
    lassoToggleHandler(){
      if (!this.lassoStatus) {
        this.toggleZoomPanLasso()
        this.disableZoom()
        this.enableLasso()
        // this.enableZoomPan()
      }
      
    },
    enableLasso(){
      const svg = d3.select('#div_graph').select("svg")
      var circles_question = svg.selectAll('.outline')
      let that = this
      var lasso_start = function () {
        // console.log(111)
        lasso.items()
          .attr('fill', "green")
          .classed('not_possible', true)
          .classed('selected', false)
      }
      var lasso_draw = function () {
        // Style the possible dots
        lasso.possibleItems()
          .classed('not_possible', false)
          .classed('possible', true)

        // Style the not possible dot
        lasso.notPossibleItems()
          .classed('not_possible', true)
          .classed('possible', false)
      }
      var lasso_end = function () {
        lasso.items()
          .classed('not_possible', false)
          .classed('possible', false)

        lasso.selectedItems()
          .classed('selected', true)
        that.selectedEntities.splice(0, that.selectedEntities.length)
        that.selectedRelations.splice(0, that.selectedRelations.length) 
        lasso.selectedItems().each(function(d){
          const label = this.nodeName 
          
          if (label == "circle") {
            console.log("adding entity" + d.id)
            that.selectedEntities.push(d.id)
          }else {
            console.log("adding Relations" + d.id)
            that.selectedRelations.push(d.id)
          }
          
        })
        // Reset the style of the not selected dots
        // lasso.notSelectedItems()
        
      }
      var lasso = d3Lasso.lasso()
        .closePathSelect(true)
        .closePathDistance(100)
        .items(circles_question)
        .targetArea(svg)
        .on('start', lasso_start)
        .on('draw', lasso_draw)
        .on('end', lasso_end)

      svg.call(lasso)
    }, 
    disableLasso() {
      const svg = d3.select('#div_graph').select("svg") 
      svg.on(".dragstart", null);
      svg.on(".drag", null);
      svg.on(".dragend", null);
    }, 
    enableZoomPan(){
      const svg = d3.select('#div_graph').select("svg") 
      svg.call(d3.zoom().on('zoom', function () {
        var scale = d3.event.transform.k,
          translate = [d3.event.transform.x, d3.event.transform.y]
        console.log(1)
        const g = svg.select("g")
        g.attr('transform', 'translate(' + translate[0] + ', ' + translate[1] + ') scale(' + scale + ')')
      }))
      .on('dblclick.zoom', null)
    },
    disableZoom() {
      const svg = d3.select('#div_graph').select("svg") 
      svg.on('.zoom', null)
    },
    toggleOverviewPanel(focus){
      if (focus == "entity") {
        const containerFocus = document.querySelector("#div_node_overview")
        const containerUnFocus = document.querySelector("#div_link_overview")
        containerFocus.style.border = "2px solid green"
        containerUnFocus.style.border = "None"
      } else{
        const containerFocus = document.querySelector("#div_link_overview")
        const containerUnFocus = document.querySelector("#div_node_overview")
        containerFocus.style.border = "2px solid green"
        containerUnFocus.style.border = "None"
      }
    },
    retrieve_types_nodes(){
      this.$store.dispatch("retrieveNodesLinksWithTypes", this.brushed)
    },
    circleUpdateMatchColor(){
      if (this.colorMapping) {
        Object.keys(this.colorMapping).forEach(category => {
          d3.selectAll('.'+category).style('fill', this.colorMapping[category])
        })
      }
    },
    recolorNode(){
      var that = this
      d3.select('#div_graph').selectAll('circle').style('fill',function(d){
      // check cold chain data
        if('resilience' in d['properties']){
          console.log(d['properties'])
          if(d['properties']['resilience']>=that.resilience_thre){
            if(that.selectedColor){
              return that.selectedColor.hex
            }else{
              return "#78b3d0"
            }
            
          }else{
            return "#b3b3b3"
          }
        }
      })
    }
  },
  watch: {
    selectedColor() {
      // this.recolorNode()
      d3.selectAll('circle').style('fill', this.selectedColor.hex)
    },
    resilience_thre(){
      this.recolorNode()
    },
    graphData () {
      // d3.select('#div_graph').html('')
      var all_resilience = []
      console.log('graphdata',this.graphData)
      this.graphData['results'][0]['data'][0]['graph']['nodes'].forEach(function (d) {
        d['status'] = 'unclicked'
        // check if this is cold chain data or not 
        if("resilience" in d['properties']){
          all_resilience.push(parseFloat(d['properties']['resilience']))
        }
        
      })
      // this.min_resilience = d3.min(all_resilience)
      this.max_resilience = d3.max(all_resilience)
      //inital the selected resilience
      KGutils.graphDataParsing(this.graphData, this.currentEntities, this.currentRelations)
      this.drawNeo4jd3()
      this.circleUpdateMatchColor()

    }, 
    selectedEntities(val) {
      if (val.length > 0) {
        this.$store.dispatch("retrieveSubTable", {entities: this.selectedEntities, relations: this.selectedRelations})
        this.$store.dispatch("retrieveNodeGeo", {node: this.selectedEntities})
      }
    }, 
    selectedRelations(val){
      if (val.length > 0) {
        this.$store.dispatch("retrieveSubTable", {entities: this.selectedEntities, relations: this.selectedRelations})
      }
    }, 
    brushed:{
      handler(val){
          console.log(val);
      },
      deep:true 
    },
    relationStatusReady(val){
      console.log("relation status: " + val) 

    },
    relationTypeData(val) {
      if(this.relationStatusReady) {
        console.log("relation type data is ready")

      }else{
        console.log("relation type data is not ready yet!")
      }
    },
    loading(val){
      this.loading_value = val
    },
    
  },
  computed: {
    ...mapState(['graphData', 'relationStatusReady', 'relationTypeData','loading', 'graphOverview', 'colorMapping']),
    HEIGHT () {
      return window.innerHeight*0.8 + 'px'
    },
    OVERVIEW_HEIGHT(){
      return window.innerHeight*0.3 + 'px'
    }
  }
}
</script>
<style>

.lasso path {
    stroke: rgb(80,80,80);
    stroke-width:2px;
}

.lasso .drawn {
    fill-opacity:.05 ;
}

.lasso .loop_close {
    fill:none;
    stroke-dasharray: 4,4;
}

.lasso .origin {
    fill:#3399FF;
    fill-opacity:.5;
}

.not_possible {
    fill: rgb(200,200,200);
}

.possible {
    fill: #EC888C;
}

.nodes .selected {
    fill: green!important;
    stroke-width: 3px!important;
    stroke: black;
}
.relationships .selected {
    stroke-width: 5px !important;
    stroke: green!important;
}
.graph-btn-container{
    position: relative; 
}
.kg-view-btn{
  margin-right: 10px;
}

.circle-button:hover{
  cursor: pointer;
}

.neo4jd3{
  margin-top:60px;
}

</style>
