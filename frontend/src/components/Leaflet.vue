<template>
    <div id="leaflet_div">
        <v-row>
            <v-col cols=6>
                 <v-switch
                    style="margin-left:20px"
                        v-model="show_eco"
                        :label="`Show Eco-Region: ${show_eco.toString()}`"
                    ></v-switch>
            </v-col>
            <v-col cols=6>
                 <v-switch
                    style="margin-left:20px"
                        v-model="show_county"
                        :label="`Show County: ${show_county.toString()}`"
                    ></v-switch>
            </v-col>
           
             <v-col cols=6>
                  <v-select
                    :items="items"
                    @change = "changeInitColor"
                    label="Color"
                    dense
                    solo
                    style="z-index:1000"
                    ></v-select>
              </v-col>
        </v-row>
        <v-row>
            <l-map style="height: 650px" :zoom="zoom" :center="center">
                <!-- <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer> -->
                <l-control-layers position="topright"></l-control-layers>
                <l-tile-layer
                    v-for="tileProvider in tileProviders"
                    :key="tileProvider.name"
                    :name="tileProvider.name"
                    :visible="tileProvider.visible"
                    :url="tileProvider.url"
                    :attribution="tileProvider.attribution"
                    layer-type="base"/>
                <l-geo-json :geojson="geojson" v-if="show_eco"></l-geo-json>
                <l-geo-json :geojson="geojson_county" v-if="show_county"></l-geo-json>
                <l-marker :v-if="show_marker" :lat-lng="marker.center" :opacity="marker.opacity" v-for ="marker in markers" :key="marker.key">
                    <l-popup :content="marker.content"/>
                </l-marker>
                <l-circle-marker
                    :v-if = "show_circle_marker"
                    v-for="circle in circles" :key="circle.key"
                    :lat-lng="circle.center"
                    :radius="circle.radius"
                    :stroke= "circle.stroke"
                    :fillColor="circle.color"
                    :color = "circle.color"
                    :fillOpacity = "circle.opacity">
                    <l-popup :content="circle.content"/>
                </l-circle-marker>
            </l-map>
          
        </v-row>
    </div>
</template>

<script>
import { latLng } from "leaflet";
import {LatLng, LMap, LTileLayer, LGeoJson,LMarker,LCircleMarker,LPopup,LControlLayers} from 'vue2-leaflet';
// import 'leaflet/dist/leaflet.css';
import {mapState} from 'vuex'
import * as d3 from 'd3'
import EcoUSDA from '../../public/USDA_ecoreg.json';
import MAPPING from '../../public/id2lonlat_cleaned.json';
import USCounties from '../../public/county_with_ecoregion_borderline.json';
export default {
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
    LMarker,
    LCircleMarker,
    LPopup,
    LControlLayers
  },
  data () {
    return {
      items: ['BestPracticesAndMandates','Organization','Program','Project','Total'],
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 4.5,
      center: [36.967483, -114.357571],
      geojson: null,
      geojson_county: null,
      show_eco: false,
      circles: null,
      all_circles: null,
      show_circle_marker: false,
      markerLatLng: [39.1014537, -84.5124602],
      selectedInit: 'Total',
      markers:null,
      show_county: false,
      show_marker: false,
      tileProviders: [
        {
          name: 'OpenStreetMap',
          visible: true,
          attribution:
            '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
          url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        },
        {
          name: 'OpenTopoMap',
          visible: false,
          url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
          attribution:
            'Map data: &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
        },
      ],
    };
  },
  async created () {
    // const response = await fetch('https://rawgit.com/gregoiredavid/france-geojson/master/regions/pays-de-la-loire/communes-pays-de-la-loire.geojson');
    this.geojson = await EcoUSDA
    this.geojson_county = await USCounties.county
    this.$store.dispatch("load_map")
    // this.show_eco = true
    // console.log(this.graphData)
    if(this.graphData){
        this.initCircleMarkerWithG()
    }else{
        // this.initCircleMarker()
    }
  },
  methods:{
    changeInitColor(val){
        this.selectedInit = val
    },
    initCircleMarker(){
        if(this.selectedInit=='Total'){
            var min = d3.min(this.mapInitialInfo, d=> {if(d.count_total>0) return d.count_total})
            var max = d3.max(this.mapInitialInfo, d=> +d.count_total)
        }else{
            var min = d3.min(this.mapInitialInfo, d=> {if(d['count_details'][this.selectedInit]>0) return d['count_details'][this.selectedInit]})
            var max = d3.max(this.mapInitialInfo, d=> +d['count_details'][this.selectedInit])
        }
        var color_mapping = d3.scaleLinear()
        .domain([min, max])
        .range(['#ffffb2','#b10026'])
        
        var circles = []
        var that = this
        this.mapInitialInfo.forEach((d,i)=>{
            // check if we have this county's lat and long 
            if(d['county_id'] in MAPPING){
                if(that.selectedInit=='Total'){
                    var val = d['count_total']
                }else{
                    var val = d['count_details'][that.selectedInit]
                }
                // don't want to draw empty county as white, ugly 
                if(val>0){
                    var ele = MAPPING[d['county_id']]
                    var temp = {
                        county_id: d['county_id'],
                        key: i,
                        center: [ele['lat'],ele['long']],
                        radius:8,
                        opacity:0.8,
                        stroke: true,
                        content: 'The '+that.selectedInit+' of '+d['county_name']+' is:'+val.toString(),
                        color: color_mapping(val)
                    }
                    circles.push(temp)
                }
            } else{
                // console.log('do not have this county lat long:',d['county_id'])
            }
        })
        this.circles = circles
        this.all_circles = circles 
        this.show_circle_marker = true
    },
    updateCircleMarker(){
       console.log(this.circles)
       console.log(this.mapQueryInfo)
       this.show_circle_marker = false
       var valid_county_id = []
       this.mapQueryInfo.forEach(d=>{
          for (let [key, value] of Object.entries(d['county'])){
            if(valid_county_id.includes(value)==false){
              valid_county_id.push(value)
            }
          }
       })

       const filtered_circles = this.all_circles.filter(d => valid_county_id.includes(d.county_id));
        this.circles = filtered_circles
        this.show_circle_marker = true

    },
    updateMarker(){
          console.log('i[date',this.mapQueryInfo)
          var output = []
          var c = 0
          this.show_marker = false
          this.mapQueryInfo.forEach(d=>{
              for (let [key, value] of Object.entries(d['county'])) {
                var ele = MAPPING[value]
                // check we have the longtitude latitude for the county
                if(value in MAPPING){
                    var temp = {
                        key: c,
                        center: [ele['lat'],ele['long']],
                        radius:8,
                        opacity:0.8,
                        stroke: true,
                        content: d['node_name']+ ' is located in '+ key,
                        color: 'red'
                    }
                    c+=1
                    output.push(temp)
                }else{
                    
                }
            }
          })
          if(output.length==0){
            alert('No relevent county info for brushed nodes!') 
          }
          this.markers = output 
          this.show_marker = true
          
    },
    initCircleMarkerWithG(){
        var nodes = this.graphData['results'][0]['data'][0]['graph']['nodes']
        console.log('initG', nodes)
        var circles = []
        var that = this
        nodes.forEach((d,i)=>{

        })
    }
  },
  computed:{
     ...mapState(['graphData', 'mapInitialInfo', 'mapQueryInfo', 'mapInQueryStatus', 'activeTab', 'ecoregion','DATABASE_NAME']),
  },
  watch:{
      DATABASE_NAME(){
        // console.log(this.DATABASE_NAME, this.mapInitialInfo)
        if(this.DATABASE_NAME=="ppod"){
            this.items= ['BestPracticesAndMandates','Organization','Program','Project','Total']
        }else{
            this.items= ['in_flow','out_flow','resilience','degree','degree_in','degree_out','strength_in','strength_out','strength','betweenness','Total']
        }
      },
      graphData(){
        console.log('graph changed', this.graphData)
      },
      mapInitialInfo(){
          this.initCircleMarker()
      },
      mapQueryInfo(){
        this.updateMarker() 
        this.updateCircleMarker()
        // this.updateMapColoring()
      },
      selectedInit(){
          this.initCircleMarker()
          this.updateCircleMarker()
      }
  }
}
</script>

<style scoped>
  @import "https://unpkg.com/leaflet@1.6.0/dist/leaflet.css";
</style>
