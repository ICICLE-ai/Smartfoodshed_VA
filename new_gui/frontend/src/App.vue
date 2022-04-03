<template>
  <v-app>
    <v-main>
      <v-row justify="center">
        <v-col cols="5" align-self="center" style="height:100%">
          <v-tabs @change="tabChange">
            <v-tab tabid="1">
              Tabular View
            </v-tab>
            <v-tab tabid="2">
              GeoMap View
            </v-tab>

            <v-tab-item>
              <table-viewer/>
            </v-tab-item>

            <v-tab-item>
              <GeoMapViewer/>
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
// import HelloWorld from './components/HelloWorld';
import TableViewer from './components/TableViewer.vue'
import KgViewer from './components/KgViewer.vue'
import GeoMapViewer from './components/GeoMapViewer.vue'
export default {
  name: 'App',

  components: {
    // HelloWorld,
    TableViewer,
    KgViewer,
    GeoMapViewer,
  },
  methods: {
    tabChange(val) {
      this.activeTab = val
      this.$store.dispatch("active_tab", this.activeTab)
    }
  },
  data: () => ({
    //
    activeTab: 0, 
  }),
};
</script>
