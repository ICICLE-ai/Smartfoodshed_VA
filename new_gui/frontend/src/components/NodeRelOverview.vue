<template>
    <v-container>
        <v-row :style="{'height': 'OVERVIEW_HEIGHT', 'margin-top':'20px'}">
            <v-col cols="6">
                <div id="div_node_overview"></div>
            </v-col>
            <v-col cols="6">
                <div id="div_link_overview"></div>
            </v-col>
        </v-row>
        <v-row
          justify="center"
        >
          <v-col
            align-self="center"
            md="1"
          >
          <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn 
                  class="ma-2 menu-btn"
                  icon
                  text
                  @click="retrieve_types_nodes"
                >
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-feature-search-outline
                  </v-icon>
                </v-btn>
              </template>
              <span>Retrieve</span>
            </v-tooltip>
          </v-col>
        </v-row>

    </v-container>
</template>

<script>
import * as d3 from 'd3'
import * as d3tip from '@/utils/d3-tip'
export default {
    props: ['graphOverview'],
    data(){
      return {
        brushed: {"entity_type": [], "relationship_type": []}, 

      }
    },
    computed: {
      OVERVIEW_HEIGHT(){
        return window.innerHeight*0.3 + 'px'
      }
    }, 
    methods: { 
        drawBarChart(div, data_, title){
        // clean the data
            let that = this
            var data = []
            const keys = Object.keys(data_);
        
            for(var i=0;i<keys.length;i++){
                data.push({'key':keys[i],'value':data_[keys[i]]})
                }

            data.sort((a, b) => a.value - b.value);
            data.reverse();
            console.log("data",data)

          var svg = d3.select(div).append("svg");
          
          const margin = 80;
          const width = 500 - 2 * margin;
          const height = 400 - 2 * margin;

          var selected_bar = []
          const chart = svg.append('g')
            .attr('transform', `translate(${margin}, ${margin})`);

          const xScale = d3.scaleBand()
            .range([0, width])
            .domain(data.map((s) => s.key))
            .padding(0.1)
          
          const yScale = d3.scaleLinear()
            .range([height, 0])
            .domain([0, d3.max(data, function(d) { return d.value; })]);

          const makeYLines = () => d3.axisLeft()
            .scale(yScale)

          var xAxis = d3.axisBottom(xScale).tickSize(0)

          chart.append('g')
          .attr("class", "axis axis--x")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis)
          .selectAll("text")  
          .style("text-anchor", "start")
          .attr("dx", "-7em")
          .attr("dy", "+.1em")
          .attr("transform", "rotate(-80)" )
          .style("font-size", "10px");

          chart.append('g')
            .call(d3.axisLeft(yScale));

          chart.append('g')
            .attr('class', 'grid')
            .call(makeYLines()
              .tickSize(-width, 0, 0)
              .tickFormat('')
            )

          const barGroups = chart.selectAll()
            .data(data)
            .enter()
            .append('g')

          barGroups
            .append('rect')
            .attr('class', 'bar')
            .attr('x', (g) => xScale(g.key))
            .attr('y', (g) => yScale(g.value))
            .attr('height', (g) => height - yScale(g.value))
            .attr('width', xScale.bandwidth())
            .on('click', function(actual,i){ 

              if (selected_bar.includes(actual.key)){
                selected_bar = selected_bar.filter(function(item) {return item !== actual.key})
                d3.select(this).attr("stroke",'none')
              }else{
                selected_bar.push(actual.key)
                d3.select(this).attr("stroke",'grey')
                d3.select(this).attr("stroke-width",'2px')
              }
              
              if (title == "Link Overview") {
                that.brushed.relationship_type = selected_bar
              }else {
                that.brushed.entity_type = selected_bar
              } 
            })
            .on('mouseenter', function (actual, i) {
            d3.selectAll('.value')
                .attr('opacity', 0)

            d3.select(this)
              .transition()
              .duration(300)
              .attr('opacity', 0.6)
              .attr('x', (a) => xScale(a.key) - 5)
              .attr('width', xScale.bandwidth() + 10)

            const y = yScale(actual.value);

            let line = chart.append('line')
                .attr('id', 'limit')
                .attr('x1', 0)
                .attr('y1', y)
                .attr('x2', width)
                .attr('y2', y)

            })
            .on('mouseleave', function () {
              d3.selectAll('.value')
                .attr('opacity', 1)

              d3.select(this)
                .transition()
                .duration(300)
                .attr('opacity', 1)
                .attr('x', (a) => xScale(a.key))
                .attr('width', xScale.bandwidth())

              chart.selectAll('#limit').remove()
              chart.selectAll('.divergence').remove()
            })

          // barGroups 
          //   .append('text')
          //   .attr('class', 'value')
          //   .attr('x', (a) => xScale(a.key) + xScale.bandwidth() / 2)
          //   .attr('y', (a) => yScale(a.value))
          //   .attr('text-anchor', 'middle')
          //   .text((a) => `${a.value}`)
          
          svg.append('text')
            .attr('class', 'label')
            .attr('x', -(height / 2) - margin)
            .attr('y', margin / 2.4)
            .attr('transform', 'rotate(-90)')
            .attr('text-anchor', 'middle')
            .text('Frequency')

          svg.append('text')
            .attr('class', 'title')
            .attr('x', width / 2 + margin)
            .attr('y', 40)
            .attr('text-anchor', 'middle')
            .text(title)
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
        graphOverview(newVal) {
            var node_overview_data = this.graphOverview['data']['entity']
            var link_overview_data = this.graphOverview['data']['relationship']
            this.drawBarChart('#div_link_overview', link_overview_data,"Link Overview")
            this.drawBarChart('#div_node_overview', node_overview_data, "Node Overview")
        }
    }
}
</script>

<style>

body {
  font-family: 'Open Sans', sans-serif;
}

div#layout {
  text-align: center;
}

div#div_node_overview {
  width: 500px;
  height: 400px;
  margin-right: 1em;
}
div#div_link_overview {
  width: 500px;
  height: 400px;
  margin-left: 1em;
}

svg {
  width: 100%;
  height: 100%;
}

.bar {
  fill: #80cbc4;
}

text {
  font-size: 12px;
  fill: #000;
}

path {
  stroke: gray;
}

line {
  stroke: gray;
}

line#limit {
  stroke: #FED966;
  stroke-width: 3;
  stroke-dasharray: 3 6;
}

.grid path {
  stroke-width: 0;
}

.grid .tick line {
  stroke: #9FAAAE;
  stroke-opacity: 0.3;
}

text.divergence {
  font-size: 14px;
  fill: #2F4A6D;
}

text.value {
  font-size: 14px;
}

text.title {
  font-size: 22px;
  font-weight: 600;
}

text.label {
  font-size: 14px;
  font-weight: 400;
}

text.source {
  font-size: 10px;
}
</style>