<template>
  <div>
    <v-app-bar
      app
    >
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-toolbar-title>ICICLE Visual Analytics V1</v-toolbar-title>
      <!-- <v-spacer></v-spacer> -->
      <div style="width:14%; margin-left:50%">
        <v-select
        
        v-model="selected_dataset"
        variant="solo"
        hint="Select A Dataset"
        persistent-hint
        :items="['ppod', 'cfs', 'ci']"
      ></v-select>
      </div>
      
    </v-app-bar>
  </div>
</template>

<script>
import {mapState} from 'vuex'
export default {
  data(){
    return {
      selected_dataset: "ppod"
    }
  }, 
  methods: {
    async fetchData(){
      await this.$store.dispatch('changeDB',{'database': this.selected_dataset})
      await this.$store.dispatch('getTableData')
      await this.$store.dispatch('getGraphOverview')
    }
  }, 
  created(){
    this.fetchData()
  },
  watch: {
    selected_dataset: function(){
      // window.location.reload();
      // d3.select('#div_graph').html('')
      this.fetchData()
    }
  },
  computed: {
    ...mapState(['BETA_ROUTE', 'DASH_ROUTE']),
    versionPrompt() {
      const currentRoute = this.$route.name
      if (currentRoute == this.DASH_ROUTE.name) {
        return "Try Dashboard Beta"
      }else {
        return "Old Version"
      }
    }
  }, 
   
}
</script>

<style>
.v-toolbar__content{
  height: 58px;
}
</style>