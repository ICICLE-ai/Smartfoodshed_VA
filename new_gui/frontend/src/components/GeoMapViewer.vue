<template>
  <div>
      <svg
        width="960px"
        height="960px"
        class="geo-map"
      >
      </svg>
  </div>
</template>

<script>
import * as d3 from 'd3'
import * as topojson from 'topojson-client'
import {mapState} from 'vuex'
// import * as d3tip from '@/utils/d3-tip'
export default {
    components: {

    }, 
    data() {
        return {
            schemes: [
                {
                    name: "RdBu", 
                    colors: [
                    "#e8e8e8", "#e4acac", "#c85a5a",
                    "#b0d5df", "#ad9ea5", "#985356",
                    "#64acbe", "#627f8c", "#574249"
                    ]
                },
            ],
            us_map_ready: false,
        }
    }, 
    methods: {
        drawMap(){
            if (! this.us_map_ready) {
                alert("map data not ready yet!");
                return
            }
            window.d3 = d3;
            const width = 700;
            const height = 900;
            const projection = d3.geoAlbersUsa().scale(800).translate([width/2, height/2])
            const path = d3.geoPath().projection(projection) 
            const svg = d3.select(".geo-map")
            
            const counties = svg.append("g")
            const states = svg.append("g")
            counties
                .selectAll("path")
                .data(topojson.feature(this.us, this.us.objects.counties).features)
                .enter().append("path")
                .attr('fill','#e4acac')
                // .attr("fill", d => color(data.get(d.id)) != null ? color(data.get(d.id)) : "white")
                .attr("stroke", "lightgrey")
                .attr("d", path)
            
            states.append("path")
                .datum(topojson.mesh(this.us, this.us.objects.states))
                .attr("fill", "none")
                .attr("stroke", "grey")
                .attr("stroke-linejoin", "round")
                .attr("d", path);

            
            svg.call(
                d3
                .zoom()
                .extent([[0, 0], [width, height]])
                .translateExtent([[0, 0], [width, height]])
                .scaleExtent([1, 4])
                .duration(500)
                .on('zoom', function() {
                    counties.attr("transform", d3.event.transform);
                    states.attr("transform", d3.event.transform);
                })
            );
        }
    },  
    created(){
        this.$store.dispatch("load_map");
        console.log(topojson);
    },
    computed: {
        ...mapState(['us']),

    },
    watch:{
        us(val){
            console.log("new val coming!!!")
            console.log(val)
            this.us_map_ready = true
            this.drawMap()
        }
    }

}
</script>

<style>

</style>