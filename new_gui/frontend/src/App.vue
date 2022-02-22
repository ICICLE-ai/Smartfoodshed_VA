<template>
  <v-app>
    <v-main>
      <v-row justify="center">
        <v-col cols="5" align-self="center">
          <table-viewer/>
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

export default {
  name: 'App',

  components: {
    // HelloWorld,
    TableViewer,
    KgViewer
  },

  data: () => ({
    //
  }),
};
</script>
