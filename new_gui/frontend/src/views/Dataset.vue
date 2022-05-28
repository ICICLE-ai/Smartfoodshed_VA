<template>
<v-app>
    <v-main>
        <v-row>
            <v-col>
                <v-btn
                    class="mx-2"
                    dark
                    large
                    color="purple"
                    @click="changeDB1"
                    >
                    <v-icon dark>
                        mdi-android
                    </v-icon>
                        PPOD
                    </v-btn>
            </v-col>
            <v-col>
                <v-btn
                    class="mx-2"
                    dark
                    large
                    color="purple"
                    @click="changeDB2"
                    >
                    <v-icon dark>
                        mdi-android
                    </v-icon>
                        Cold Chain Dataset
                </v-btn>
            </v-col>
        </v-row>
    </v-main>
</v-app>

</template>
<script>
export default{
    data(){
        return{
            database: ""
        }
    },
    methods:{ 
        changeDB1(){
            this.database = "ppod"
            this.goToNext()
        },
        changeDB2(){
            this.database = "cfs"
            this.goToNext()
        },
        async goToNext(){
            await this.$store.dispatch('changeDB',{'database': this.database})
            await this.$store.dispatch('getTableData')
            await this.$store.dispatch('getGraphOverview')
            this.$router.push('Dashboard')
        }
    },
    watch:{ 
        
    }
}
</script>
