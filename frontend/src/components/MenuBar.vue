<template>
  <div>
    <v-card
      class="dashboard-menu"
      outlined
    >
      <v-row
        v-for="menu in menu.menuList"
        :key="menu.label"
        no-gutters
      >
        <v-col>
          <MenuBtn
            :item="menu"
          />

        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import {mapState} from 'vuex'
import MenuBtn from '@/components/MenuBtn'
export default {
  data(){
    return {
      items: []
    }
  },
  computed: {
    ...mapState(['menu'])
  },
  components: {
    MenuBtn
  },
  created(){
    
    console.log(this.menu);
  }
}
</script>

<style scoped>
  .dashboard-menu{
    position: fixed; 
    top: 60px;
    left: 10px;
  }
</style>