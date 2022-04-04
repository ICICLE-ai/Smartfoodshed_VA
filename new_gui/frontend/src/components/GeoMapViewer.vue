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
import * as d3tip from '@/utils/d3-tip'
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
            highLightInfo: {}, 
            warningMsgStack: []
        }
    }, 
    methods: {
        drawMap(){
            const that = this 
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
            if (that.mapInQueryStatus && Object.keys(that.highLightInfo).length == 0) {
                alert("No geo info about the selected node")
            }
            counties
                .selectAll("path")
                .data(topojson.feature(this.us, this.us.objects.counties).features)
                .enter().append("path")
                .attr("class", "county-path")
                .attr("id", d=>{
                    let str = ""
                    if(+d.id < 10000) {
                        str = "0" + d.id
                    }else{
                        str = str + d.id
                    }
                    return `county-${str}`})
                .attr('fill', d => {
                    if (that.mapInQueryStatus) {
                        if (that.highLightInfo) {
                            const county_id = d.id 
                            if(county_id in this.highLightInfo){
                                return "#e4acac"
                            } else {
                                return "white"
                            }
                        } else {
                            return "white"
                        }
                    }else {
                        return '#e4acac'
                    }
                })
                // .attr("fill", d => color(data.get(d.id)) != null ? color(data.get(d.id)) : "white")
                .attr("stroke", "lightgrey")
                .attr("d", path)
                .on("mouseover", function(d){
                    d3.select(this).raise()
                    const county_id = d.id  
                    let idStr = ""
                    if (county_id < 10000) {
                        idStr = "0" + county_id
                    }else{
                        idStr = "" + county_id 
                    }
                    if (that.mapInQueryStatus && that.highLightInfo && that.highLightInfo[idStr] != null) {
                        that.mapTip.show(that.highLightInfo[idStr])
                    }
                    d3.select(this).attr("stroke", "green")
                    // that.mapTip.show()
                })
                .on("mouseout", function(d){
                    
                    d3.select(this).attr("stroke", "lightgrey")
                    that.mapTip.hide()
                })
            
            states.append("path")
                .datum(topojson.mesh(this.us, this.us.objects.states))
                .attr("class", "state-path")
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
            )
            svg.call(that.mapTip)
        },
        updateQueryInfo(){
            //container = this.highLightInfo 
            /*
            * {
                county_id: [node_id, ...]
            }
            */
            this.highLightInfo = {};
            console.log(this.mapQueryInfo)
            if (this.mapQueryInfo.length > 0) {
               this.mapQueryInfo.forEach(obj => {
                console.log(obj)
                const node_id = obj.node_id; 
                const county_id = obj.county_id
                if (node_id != null && county_id.length > 0) {
                    county_id.forEach(county => {
                        if (county in this.highLightInfo) {
                            this.highLightInfo[county].push(node_id)
                        }else{
                            this.highLightInfo[county] = [node_id] 
                        }
                    })
                }
            })
            }
            console.log(this.highLightInfo)
            
            
        }, 

        updateMapColoring(){
            d3.selectAll(".county-path").attr("fill", "white") 
            if (Object.keys(this.highLightInfo).length == 0) {
                if (this.activeTab == 1) {
                    alert("No geo info about the selected node")
                } else {
                    if (this.warningMsgStack.length == 0) {
                        this.warningMsgStack.push("No geo info about the selected node")
                    }
                }
            }else {
                Object.keys(this.highLightInfo).forEach(countyId => {
                    d3.select(`#county-${countyId}`).attr("fill", "#e4acac")
                })
                if (this.warningMsgStack.length > 0) {
                        this.warningMsgStack.pop()
                }
            }
        }, 
    },  
    created(){
        this.$store.dispatch("load_map")
        console.log(topojson);
        this.mapTip = d3tip()
            .attr('class', 'd3-tip-map')
            .offset([-10, 80])
            .html(function(d) {
              return `
                <div class="tip-container">
                    <p>${d}</p>
                </div>
              `;
    })
    },
    computed: {
        ...mapState(['us', 'mapInitialInfo', 'mapQueryInfo', 'mapInQueryStatus', 'activeTab']),

    },
    watch:{
        us(val){
            console.log("new val coming!!!")
            console.log(val)
            this.us_map_ready = true
            if (this.mapQueryInfo) {
                this.updateQueryInfo() 
            }
            this.drawMap()
            // this.updateMapColoring()
        },
        mapInitialInfo(val,) {
            console.log("Map data initialized")
            console.log(val)
            
        }, 
        mapQueryInfo(val, ){
            console.log("new query Info")
            console.log(val)
            this.updateQueryInfo() 
            this.updateMapColoring()
        },
        activeTab(val) {
            if (val == 1 && this.warningMsgStack.length > 0) {
                while (this.warningMsgStack.length > 0) {
                    let msg = this.warningMsgStack.pop(); 
                    alert(msg)
                }
            }
        }
    }

}
</script>

<style>
.d3-tip-map{
    background-color: rgba(252, 247, 241, 0.7);
    background-opacity: 0.2;
    width: 130px; 
    height: 70px;
    border-radius: 5px;
}
.tip-container{ 
    text-align: center;
}
</style>