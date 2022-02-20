<template>
    <div class="fullHeight">
        <div id="div_graph" class="fullHeight" :style="{'height': HEIGHT}"></div>
    </div>
</template>

<script>
import * as Neo4jd3 from '../js/Neo4D3'
import * as d3Lasso from 'd3-lasso'
import * as d3 from 'd3'
export default{
  components: {

  },
  data () {
    return {
      // graphData:{}
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
          that.dbclick(node)
        },
        onNodeMouseEnter: function (node) {
          that.hover_node = node
        },
        onNodeClick: function (node) {
        }
      })

      const svg = d3.select('#div_graph').select("svg")
      var circles_question = svg.selectAll('circle')
      console.log(circles_question)
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
        console.log("!!!!!!!!!!!!")
        console.log(lasso.notSelectedItems())
        lasso.items()
          .classed('not_possible', false)
          .classed('possible', false)

        // Style the selected dots
        lasso.selectedItems()
          .classed('selected', true)
          .style('fill', "green")

        // Reset the style of the not selected dots
        lasso.notSelectedItems()
        //   .attr('r', 3.5)
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
    }
  },
  watch: {
    graphData () {
      // console.log(this.graphData)
      // console.log(this.graphData['results'][0]['data'][0]['graph']['nodes'])
      this.graphData['results'][0]['data'][0]['graph']['nodes'].forEach(function (d) {
        // this.graphData['nodes'].forEach(function(d){
        // console.log(d)
        d['status'] = 'unclicked'
      })
      this.drawNeo4jd3()
    }
  },
  mounted () {

  },
  computed: {
    graphData () {
      return this.$store.state.graphData
    },
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

.selected {
    fill: steelblue;
}
</style>
