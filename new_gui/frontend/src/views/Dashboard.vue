<template>
  <v-app>
    <v-main>
      <v-row justify="center">
        <v-col cols="5" align-self="center">
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
        </v-col>
        <v-col cols="7">
          <kg-viewer/>
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
