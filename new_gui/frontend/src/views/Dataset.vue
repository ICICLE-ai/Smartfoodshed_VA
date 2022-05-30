<template>
<v-app>
    <v-main>
        <v-row>
            <v-col key="1" cols="5">
                <v-hover v-slot="{hover}">
                    <v-card
                    :loading="loading1"
                    :elevation="hover ? 12 : 2"
                    :class="{ 'on-hover': hover }"
                    @click="changeDB1"
                    >
                        <v-img
                            src="https://images.squarespace-cdn.com/content/v1/59a9c2ff8dd041f31701dea3/1602745366392-62IIKPSCRXAO464UJ4HA/IC-FOODS+Logo+Better.png?format=1500w"
                            height="400px"
                        ></v-img>
                        <v-card-title>
                            Explore PPOD Dataset 
                            <v-icon> mdi-arrow-right-thick</v-icon>
                        </v-card-title>
                    </v-card>
                </v-hover>  
            </v-col>
            <v-col key="2" cols="5">
                <v-hover v-slot="{hover}">
                    <v-card
                    :loading = "loading2"
                    :elevation="hover ? 12 : 2"
                    :class="{ 'on-hover': hover }"
                    @click="changeDB2"
                    >
                        <v-img
                            src="https://www.qualityassurancemag.com/fileuploads/publications/29/issues/103585/articles/images/AdobeStock_280800711_fmt.jpg"
                            height="400px"
                        ></v-img>
                        <v-card-title>
                            Explore CFS Dataset 
                            <v-icon> mdi-arrow-right-thick</v-icon>
                        </v-card-title>
                    </v-card>
                </v-hover>  
            </v-col>
        </v-row>
    </v-main>
</v-app>

</template>
<script>
export default{
    data(){
        return{
            database: "",
            loading1: false,
            loading2: false
        }
    },
    methods:{ 
        changeDB1(){
            this.database = "ppod"
            this.loading1 = true
            this.goToNext()
            
        },
        changeDB2(){
            this.database = "cfs"
            this.loading2 = true
            this.goToNext()
        },
        async goToNext(){
            await this.$store.dispatch('changeDB',{'database': this.database})
            await this.$store.dispatch('getTableData')
            await this.$store.dispatch('getGraphOverview')
            this.loading1 = false
            this.loading2 = false
            this.$router.push('Dashboard')
        }
    },
    watch:{ 
        
    }
}
</script>
<style scoped>
.v-card {
  transition: opacity .4s ease-in-out;
}

.v-card:not(.on-hover) {
  opacity: 0.6;
 }

.show-btns {
  color: rgba(255, 255, 255, 1) !important;
}
</style>
