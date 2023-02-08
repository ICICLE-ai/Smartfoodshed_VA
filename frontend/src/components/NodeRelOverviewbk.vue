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
        graphOverview(newVal) {
            console.log(newVal) 
            var node_overview_data = this.graphOverview['data']['entity']
            var link_overview_data = this.graphOverview['data']['relationship']
            console.log('fff', node_overview_data, link_overview_data)
            this.drawBarChart('#div_link_overview', link_overview_data)
            this.drawBarChart('#div_node_overview', node_overview_data)
        }
    }
}
</script>

<style>

</style>