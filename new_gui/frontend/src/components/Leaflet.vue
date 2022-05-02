<template>
    <div>
        <v-row>
            <v-col cols=6>
                 <v-switch
                    style="margin-left:20px"
                        v-model="show_eco"
                        :label="`Show Eco-Region: ${show_eco.toString()}`"
                    ></v-switch>
            </v-col>
           
             <v-col cols=6>
                  <v-select
                    :items="items"
                    @change = "changeInitColor"
                    label="Color"
                    dense
                    solo
                    ></v-select>
              </v-col>
        </v-row>
        <v-row>
            <l-map style="height: 650px" :zoom="zoom" :center="center">
                <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
                <l-geo-json :geojson="geojson" v-if="show_eco"></l-geo-json>
                <!-- <l-marker :lat-lng="markerLatLng"></l-marker> -->
                <l-circle-marker
                    :v-if = "show_marker"
                    v-for="circle in circles" :key="circle.key"
                    :lat-lng="circle.center"
                    :radius="circle.radius"
                    stroke= true
                    :fillColor="circle.color"
                    :color = "circle.color"
                    weight=2
                    :fillOpacity = "circle.opacity">
                    <l-popup :content="circle.content"/>
                </l-circle-marker>
            </l-map>
          
        </v-row>
    </div>
</template>

<script>
import { latLng } from "leaflet";
import {LatLng, LMap, LTileLayer, LGeoJson,LMarker,LCircleMarker,LPopup} from 'vue2-leaflet';
// import 'leaflet/dist/leaflet.css';
import {mapState} from 'vuex'
import * as d3 from 'd3'
import EcoUSDA from '../../public/USDA_ecoreg.json';
import MAPPING from '../../public/id2lonlat_cleaned.json';
export default {
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
    LMarker,
    LCircleMarker,
    LPopup
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
      show_eco: false,
      circles: null,
      show_marker: false,
      markerLatLng: [39.1014537, -84.5124602],
      selectedInit: 'Total',
    };
  },
  async created () {
    // const response = await fetch('https://rawgit.com/gregoiredavid/france-geojson/master/regions/pays-de-la-loire/communes-pays-de-la-loire.geojson');
    this.geojson = await EcoUSDA
    this.$store.dispatch("load_map")
    // this.show_eco = true
  },
  methods:{
    changeInitColor(val){
        this.selectedInit = val
    },
    initMarker(){
        console.log(this.mapInitialInfo)
        if(this.selectedInit=='Total'){
            var min = d3.min(this.mapInitialInfo, d=> {if(d.count_total>0) return d.count_total})
            var max = d3.max(this.mapInitialInfo, d=> +d.count_total)
        }else{
            var min = d3.min(this.mapInitialInfo, d=> {if(d['count_details'][this.selectedInit]>0) return d['count_details'][this.selectedInit]})
            var max = d3.max(this.mapInitialInfo, d=> +d['count_details'][this.selectedInit])
        }
        var color_mapping = d3.scaleLinear()
        .domain([min, max])
        .range(['#9ecae1','#084594'])
        
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
                        key: i,
                        center: [ele['lat'],ele['long']],
                        radius:8,
                        opacity:0.8,
                        content: d['county_name']+':'+val.toString(),
                        color: color_mapping(val)
                    }
                    circles.push(temp)
                }
            } else{
                console.log('do not have this county lat long:',d['county_id'])
            }
        })
        this.circles = circles
        this.show_marker = true
        // var color = d3.scaleLinear()
        // .domain(d3.)
        // var val = this.mapInitialInfo
        // var colorMapping = {}

        // if(this.selectedInit=="Total"){
        //     val.forEach(d=>{
        //         colorMapping[d['county_id']] = d['count_total']
        //     })
        // }else{
        //     val.forEach(d=>{
        //         colorMapping[d['county_id']] = d['count_details'][this.selectedInit]
        //     })
        // }
          
      }
  },
  computed:{
     ...mapState(['us', 'mapInitialInfo', 'mapQueryInfo', 'mapInQueryStatus', 'activeTab', 'ecoregion']),
  },
  watch:{
      us(){
          console.log('test', this.us)
      },
      mapInitialInfo(){
          this.initMarker()
          console.log('test',this.mapInitialInfo)
      },
      selectedInit(){
          this.initMarker()
      }
  }
}
</script>

<style>
@import "https://unpkg.com/leaflet@1.6.0/dist/leaflet.css";

</style>
