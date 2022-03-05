<template>
    <div class="fullHeight" style="position:relative">
        <div
          class="graph-btn-container"
        >
        <v-btn
            small
            @click="resetGraphTableHandler"
            style="margin-left: 10px"
            class="kg-view-btn"
          >
            Reset
        </v-btn>
        <v-btn
          small
          @click="zoomPanToggleHandler"
          :color="zoomPanColor"
          class="kg-view-btn"
        >
          <v-icon>
            mdi-arrow-expand-all
          </v-icon>
        </v-btn>
        <v-btn
          small
          @click="lassoToggleHandler"
          :color="lassoColor"
          class="kg-view-btn"
        >
          <v-icon>
            mdi-lasso
          </v-icon>
        </v-btn>
        </div>
        <div id="div_graph" class="fullHeight" :style="{'height': HEIGHT}"></div>   
        
    </div>
</template>

<script>
import * as Neo4jd3 from '../js/Neo4D3'
import * as d3Lasso from 'd3-lasso'
import * as d3 from 'd3'
import * as KGutils from '@/utils/KGutils.js'
import {mapState} from 'vuex'
export default{
  components: {

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
    }
  },
  created () {
    this.$store.dispatch('getGraphData')
    window['d3'] = d3
  },
  methods: {
    drawNeo4jd3 () {
      // console.log(this.graphData)
      var that = this
      var width = 600, height = 400
      //   const svg = d3.select('#div_graph').append('svg')
      //     .attr('viewBox', [0, 0, width, height])
      var neo4jd3 = Neo4jd3.default('#div_graph', {
        neo4jData: that.graphData,
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
          console.log(that.relationStatusReady)
          // Create dummy data
          var data = { b: {action: "remove", value: 10, pos:0} } // only two operations 

          if(that.relationStatusReady==false){
            // render the loading panel 
          }else{
            let relation_data = that.relationTypeData['results'][0]['data'][0]['graph']['nodes'][idx]['relationship_types']
            // get the sum of all rel counts 
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

          // set the color scale
          var color = d3.scaleOrdinal()
            .domain(data)
            .range(["#94B49F", "#BB6464"])


            // Compute the position of each group on the pie:
          var pie = d3.pie()
            .sort(null) //avoiding to sort the pie, make sure the remove button in the same position 
            .value(function(d) {return d.value.value; })
          var data_ready = pie(d3.entries(data))
          
          // sort data to make sure the remove always appear in the same position 
          // data_ready.sort((a, b) => (a.index > b.index) ? 1 : -1)
    
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

            // hovering effect 
            operation_buttons.on('mouseover', function(d){
              console.log("mouseover")
              d3.select(this).style('opacity',1)
            })
            .on('mouseout',function(d){
              d3.select(this).style('opacity',0.7)
            })
            .on('click', function(d,i){
              let clicked_node_id = node['id']
              const action = d.data.value.action 
              if (action == "expand"){
                that.$store.dispatch("node_expand", {node_id: clicked_node_id})
              }else {
                that.$store.dispatch("node_remove", {node_id: clicked_node_id})
              }
            })
        }
      })
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

        const g = svg.select("g")
        g.attr('transform', 'translate(' + translate[0] + ', ' + translate[1] + ') scale(' + scale + ')')
      }))
      .on('dblclick.zoom', null)
    },
    disableZoom() {
      const svg = d3.select('#div_graph').select("svg") 
      svg.on('.zoom', null)
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
    relationStatusReady(val){
      console.log("relation status: " + val) 
    },
    relationTypeData(val) {
      if(this.relationStatusReady) {
        console.log("relation type data is ready")
        console.log(val)
      }else{
        console.log("relation type data is not ready yet!")
      }
    }
  },
  beforeMounted() {

  }, 
  mounted () {

  },
  computed: {
    ...mapState(['graphData', 'relationStatusReady', 'relationTypeData']),
    HEIGHT () {
      return window.innerHeight + 'px'
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
</style>
