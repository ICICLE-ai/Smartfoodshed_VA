<template>
  <div>
    <v-app-bar
      app
      dense
    >
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
      <v-toolbar-title>ICICLE Visual Analytics Prototype</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        text
        rounded
        color="purple"
        @click="versionSwitch"
      >
        {{versionPrompt}}
      </v-btn>
    </v-app-bar>
  </div>
</template>

<script>
import {mapState} from 'vuex'
export default {
  data(){
    return {
      // versionPrompt: "Try Dashboard beta", 
    }
  }, 
  methods: {
    versionSwitch() {
      const currentRoute = this.$route.name
      if (currentRoute == this.DASH_ROUTE.name) { 
        // this.versionPrompt = "Try Dashboard beta"
        this.$router.push(this.BETA_ROUTE.route)
      }else {
        // this.versionPrompt == "Old Version" 
        this.$router.push(this.DASH_ROUTE.route)
      }
      
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

</style>