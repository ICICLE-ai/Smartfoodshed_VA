<template>
  <v-app style="height:100%">
    <v-main style="padding:0px; height:100%">
      
      <v-row justify="center" style="height:100%">
        <v-col cols="5" align-self="center" style="height:100%">
          <v-card style="height:100%">
            <v-tabs>
                <v-tab>
                  Tabular View
                </v-tab>
                <v-tab>
                  GeoMap View
                </v-tab>
                <v-tab-item>
                  <table-viewer/>
                </v-tab-item>
                <v-tab-item>
                  <leaflet/>
                </v-tab-item>
              </v-tabs>
          </v-card>
        </v-col>
        <v-col cols="7">
          <v-card style="height:100%">
            <v-card-title>Graph View</v-card-title>
            <kg-viewer/>
          </v-card>
          
          
        </v-col>
      </v-row>
    </v-main>
  </v-app>
</template>

<script>
import TableViewer from '@/components/TableViewer.vue'
import KgViewer from '@/components/KgViewer.vue'
import Leaflet from '@/components/Leaflet.vue'
export default {
  name: 'App',

  components: {
    TableViewer,
    KgViewer,
    Leaflet
  },

  data: () => ({
    //
  }),
};
</script>
