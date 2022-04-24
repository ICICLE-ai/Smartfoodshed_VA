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
            console.log("data",data)

          const svg = d3.select('svg');
          const svgContainer = d3.select('#container');
          
          const margin = 80;
          const width = 1000 - 2 * margin;
          const height = 600 - 2 * margin;

          const chart = svg.append('g')
            .attr('transform', `translate(${margin}, ${margin})`);

          const xScale = d3.scaleBand()
            .range([0, width])
            .domain(data.map((s) => s.key))
            .padding(0.4)
          
          const yScale = d3.scaleLinear()
            .range([height, 0])
            .domain([0, 100]);

          const makeYLines = () => d3.axisLeft()
            .scale(yScale)

          chart.append('g')
            .attr('transform', `translate(0, ${height})`)
            .call(d3.axisBottom(xScale));

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
            .on('mouseenter', function (actual, i) {
              d3.selectAll('.value')
                .attr('opacity', 0)

              d3.select(this)
                .transition()
                .duration(300)
                .attr('opacity', 0.6)
                .attr('x', (a) => xScale(a.key) - 5)
                .attr('width', xScale.bandwidth() + 10)

              const y = yScale(actual.value)

              line = chart.append('line')
                .attr('id', 'limit')
                .attr('x1', 0)
                .attr('y1', y)
                .attr('x2', width)
                .attr('y2', y)

              barGroups.append('text')
                .attr('class', 'divergence')
                .attr('x', (a) => xScale(a.key) + xScale.bandwidth() / 2)
                .attr('y', (a) => yScale(a.value) + 30)
                .attr('fill', 'white')
                .attr('text-anchor', 'middle')
                .text((a, idx) => {
                  const divergence = (a.value - actual.value).toFixed(1)
                  
                  let text = ''
                  if (divergence > 0) text += '+'
                  text += `${divergence}%`

                  return idx !== i ? text : '';
                })

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

          barGroups 
            .append('text')
            .attr('class', 'value')
            .attr('x', (a) => xScale(a.key) + xScale.bandwidth() / 2)
            .attr('y', (a) => yScale(a.value) + 30)
            .attr('text-anchor', 'middle')
            .text((a) => `${a.value}%`)
          
          svg
            .append('text')
            .attr('class', 'label')
            .attr('x', -(height / 2) - margin)
            .attr('y', margin / 2.4)
            .attr('transform', 'rotate(-90)')
            .attr('text-anchor', 'middle')
            .text('Love meter (%)')

          svg.append('text')
            .attr('class', 'label')
            .attr('x', width / 2 + margin)
            .attr('y', height + margin * 1.7)
            .attr('text-anchor', 'middle')
            .text('Languages')

          svg.append('text')
            .attr('class', 'title')
            .attr('x', width / 2 + margin)
            .attr('y', 40)
            .attr('text-anchor', 'middle')
            .text('Most loved programming languages in 2018')

          svg.append('text')
            .attr('class', 'source')
            .attr('x', width - margin / 2)
            .attr('y', height + margin * 1.7)
            .attr('text-anchor', 'start')
            .text('Source: Stack Overflow, 2018')
          
                
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
            // this.drawBarChart('#div_link_overview', link_overview_data)
            this.drawBarChart('#div_node_overview', node_overview_data)
        }
    }
}
</script>

<style>

</style>