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
            sm="3"
            cols="11"
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
            <!-- <v-btn
              small
              class="kg-view-btn"
              @click="resetGraphTableHandler"
              >
              Reset
            </v-btn> -->
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

            <!-- <v-btn
              small
              @click="zoomPanToggleHandler"
              :color="zoomPanColor"
              class="kg-view-btn"
              >
              <v-icon>
                mdi-arrow-expand-all
              </v-icon>
            </v-btn> -->
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
              <span>Node Link Overview</span>
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

            <v-slider
              v-model="user_defined_thre"
              :thumb-size="24"
              @click="changeThreshold"
              thumb-label="always"
              v-show="showMaxRetrieve"
            ></v-slider>
            <!-- <v-btn
                small
                class="kg-view-btn"
                @click="lassoToggleHandler"
                :color="lassoColor"
              >
                <v-icon>
                  mdi-lasso
                </v-icon>
            </v-btn> -->
          </v-col>
        </v-row>
        </v-container>
        </div>
        <node-rel-overview
          v-show="showOverview"
          :graphOverview="graphOverview"
        />
        <div id="div_graph" class="fullHeight" :style="{'height': HEIGHT}"></div>   
        <v-overlay :value="loading_value">
        <v-progress-circular
          indeterminate
          size="64"
        ></v-progress-circular>
      </v-overlay>
    </div>
</template>

<script>
import * as Neo4jd3 from '../js/Neo4D3'
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
    }
  },
  created () {
    this.$store.dispatch('getGraphOverview')
    window['d3'] = d3
    this.tip = d3tip()
            .attr('class', 'd3-tip')
            .offset([-10, 80])
            .html(function(d) {
              return "<strong>Relation: </strong>" + d + "<br></span>";
    })
    console.log(document.querySelector("#div_graph"));
    
  },
  methods: {
    changeThreshold(){
      // change user define threshold for how many nodes we want to expand 
      this.$store.dispatch('setExpandTh', this.user_defined_thre)
    },
    drawNeo4jd3 () {
      var that = this
      d3.selectAll(".d3-tip").remove()


      if(this.neo4jd3 == null){
        var neo4jd3 = Neo4jd3.default('#div_graph', {
          neo4jData: this.graphData,
          nodeRadius: 30,
          infoPanel: false,

          onNodeDoubleClick: function (node) {
            // that.dbclick(node)
          },
          onNodeMouseEnter: function (node) {
            that.hover_node = node
          },
          onNodeClick: function (node,idx) {
            // console.log(node,id)
            // Create dummy data
            console.log(node)
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
              console.log(that.relationTypeData['results'][0]['data'][0]['graph']['nodes'])
              console.log(idx)
              let filtered_relation_type_data = that.relationTypeData['results'][0]['data'][0]['graph']['nodes'].filter(d => d.id == node.id)
              let relation_data = filtered_relation_type_data[0]['relationship_types']
              // get the sum of all rel counts 
              const sumValues = obj => Object.values(obj).reduce((a, b) => a + b);
              const total_c  = sumValues(relation_data)
              // generate the dount data
              for (const [key, value] of Object.entries(relation_data)) {
                data[key] = {action: key, value: (value/total_c)*30}
              }
              console.log("check data")
              console.log(data)
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
                console.log(d)
                that.tip.hide(d.data.value.action)
                if (action == "remove"){
                  // tip.hide(d.data.value.action)
                  that.$store.dispatch("node_remove", {node_id: clicked_node_id})
                }else {
                  
                  console.log(d.data.value.action)
                  that.$store.dispatch("node_expand", {node_id: clicked_node_id, relation: d.data.key})
                }
              })
          }
      })
        this.neo4jd3 = neo4jd3
      }else{
        this.neo4jd3.updateWithNeo4jData(this.graphData)
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
        console.log(111)
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
    drawBarChart(div, data_){
      // clean the data
      let that = this
      var data = []
      const keys = Object.keys(data_);
      
      for(var i=0;i<keys.length;i++){
        data.push({'key':keys[i],'value':data_[keys[i]]})
        }

      data.sort((a, b) => a.value - b.value);
      data.reverse();

      var margin = {top: 20, right: 30, bottom: 90, left: 70},
      margin2 = { top: 230, right: 30, bottom: 10, left: 70 },
      width = window.innerWidth*(7/12)*0.5 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom,
      height2 = 300 - margin2.top - margin2.bottom;

      var svg = d3.select(div).append("svg")
      // .append("rect")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom);

      var focus = svg.append("g")
      .attr("class", "focus")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var context = svg.append("g")
      .attr("class", "context")
      .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");


      // set the ranges
      var x_domain = 0;
      var temp_data = 0;
      var x = d3.scaleBand().range([0, width]).padding(0.1);
      var y = d3.scaleLinear().range([height, 0]);
      // set brushable ranges
      var x2 = d3.scaleBand().range([0, width]).padding(0.1);
      var y2 = d3.scaleLinear().range([height2, 0]);

      var xAxis = d3.axisBottom(x).tickSize(0),
          xAxis2 = d3.axisBottom(x2).tickSize(0),
          yAxis = d3.axisLeft(y);

      var brush = d3.brushX()
          .extent([[0, 0], [width, height2]])
          .on("brush end", brushed);

      
      var bars1;
      var bars2;
      // Scale the range of the data in the domains
                      temp_data = data;
                      x_domain = data.map(function(d) { return d.key; })
                      // console.log(x_domain)
                      x.domain(data.map(function(d) { return d.key; }));
                      y.domain([0, d3.max(data, function(d) { return d.value; })]);
                      x2.domain(x.domain());
                      y2.domain(y.domain());
                      
                      var temp_rt =  drawBar1(focus, data)
                      var bars1 = temp_rt[0]
                      var bar1bars = temp_rt[1]
                      var bar1x = temp_rt[2]
                      var bar1y = temp_rt[3]
      var bars2 = context.selectAll("rect").data(data).enter().append("rect");

                      bars2.attr("class", "bar").attr("x", function(d) { return x2(d.key); })
                          .attr("y", function(d) { return y2(d.value); })
                          .attr("width", x2.bandwidth())
                          .attr("height", function(d){ return height2-y2(d.value); })
                          .attr('fill','steelblue');

                      focus.append("path")
                      .datum(data)
                      .attr("class", "bar")
                      .attr("d", bars1);

                      context.append("path")
                          .datum(data)
                          .attr("class", "bar")
                          .attr("d", bars2);

                      context.append("g")
                          .attr("class", "axis axis--x")
                          .attr("transform", "translate(0," + height2 + ")");
                          // .call(xAxis2);

                      context.append("g")
                          .attr("class", "brush")
                          .call(brush)
                          .call(brush.move, x.range());

                      svg.append("rect")
                          .attr("width", width)
                          .attr("height", height)
                          .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
                          .attr('fill','none')
              function drawBar1(focus, data){

                  bars1 = focus.selectAll("rect").data(data).enter().append("rect");

                  bar1bars = bars1.attr("class", "bar").attr("x", function(d) { return x(d.key); })
                  .attr("y", function(d) { return y(d.value); })
                  .attr("width", x.bandwidth())
                  .attr("height", function(d){ return height-y(d.value); })
                  .attr('fill','steelblue')

                  bar1x = focus.append("g")
                      .attr("class", "axis axis--x")
                      .attr("transform", "translate(0," + height + ")")
                      .call(xAxis)
                      .selectAll("text")  // NAME 
                      .style("text-anchor", "start")
                      .attr("dx", "+.8em")
                      .attr("dy", "+.1em")
                      .attr("transform", "rotate(-90)" );

                  bar1y = focus.append("g")
                      .attr("class", "axis axis--y")
                      .call(yAxis);

                  // Create the Focus Y Axis Text Label
                  focus.append("text")
                  .style("font", "10px arial")
                  .attr("transform", "rotate(-90)")
                  .attr("y", 0 - margin.left)
                  .attr("x",0 - (height / 2))
                  .attr("dy", "2em")
                  .style("text-anchor", "middle")
                  .text("Frequency"); 

                  return [bars1, bar1bars, bar1x, bar1y];
                  
                  }
                  function brushed() {
                    if (d3.event.sourceEvent && d3.event.sourceEvent.type === "zoom") return; // ignore brush-by-zoom

                    bar1bars.remove()
                    bar1x.remove()
                    bar1y.remove()

                    var s = d3.event.selection || x2.range();
                    var temp_domain = x_domain.slice(Math.round(s[0]/x2.step()), Math.round(s[1]/x2.step()))
                    x.domain(temp_domain);
                    console.log(temp_domain)
                    const container = d3.select(this).node().parentElement.parentElement.parentElement.id;
                    if(container == "div_node_overview"){
                      that.brushed['entity_type'] = temp_domain;
                      that.brushed['relationship_type'] = [];
                      that.toggleOverviewPanel("entity")
                    }else if (container == "div_link_overview"){
                      that.brushed['relationship_type'] = temp_domain; 
                      that.brushed['entity_type'] = [];
                      that.toggleOverviewPanel("relationship")
                    }else{
                      alert("error finding container")
                    }
                    var new_temp_data = temp_data.slice(Math.round(s[0]/x2.step()), Math.round(s[1]/x2.step()))

                    var temp_rt =  drawBar1(focus, new_temp_data)
                    bars1 = temp_rt[0]
                    bar1bars = temp_rt[1]
                    bar1x = temp_rt[2]
                    bar1y = temp_rt[3]

                    focus.select("bar").attr("d", bars1);
                    focus.select("axis axis--x").call(xAxis);
                  
                }
                
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
    }
  },
  watch: {
    graphData () {
      console.log(this.graphData)
      this.graphData['results'][0]['data'][0]['graph']['nodes'].forEach(function (d) {
        d['status'] = 'unclicked'
      })
      console.log("check graph data")
      console.log(this.graphData)
      KGutils.graphDataParsing(this.graphData, this.currentEntities, this.currentRelations)
      this.drawNeo4jd3()
    }, 
    selectedEntities(val) {
      if (val.length > 0) {
        console.log("retrieving data now!!!")
        console.log(val.length)
        console.log(this.selectedEntities)
        console.log(this.selectedRelations)
        console.log("****************")
        console.log(val)
        this.$store.dispatch("retrieveSubTable", {entities: this.selectedEntities, relations: this.selectedRelations})
        this.$store.dispatch("retrieveNodeGeo", {node: this.selectedEntities})
      }
    }, 
    selectedRelations(val){
      if (val.length > 0) {
        console.log("****************")
        console.log(val.length)
        console.log(val) 
        console.log("retrieving data now!!!")
        console.log(this.selectedEntities)
        console.log(this.selectedRelations)
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
    ...mapState(['graphData', 'relationStatusReady', 'relationTypeData','loading', 'graphOverview']),
    HEIGHT () {
      return window.innerHeight*0.7 + 'px'
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
    top: 30px;
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
