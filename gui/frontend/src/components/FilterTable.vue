<template>
    <div>
        <div>
            <vue-tabulator  ref="tabulator" v-model="dados" :options="options" v-if="showTable"/>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
import vueTabulator from "vue-tabulator";
Vue.use(vueTabulator, { name: "vue-tabulator" });

export default{
    data(){
        return{
            dados:[],
            options: [],
            showTable:false
        }
    },
    created(){
        // this.test()
        this.$store.dispatch('getTableData')
        
    },
    methods:{
    },
    watch:{
        tableData(){
            console.log(this.tableData)
            this.options= this.tableData['option']
            this.dados = this.tableData['data']
            // console.log(this.options, this.dados)
            this.showTable = true
        }
    },
    mounted(){
        // let recaptchaScript = document.createElement('script')
        // recaptchaScript.setAttribute('src', 'https://oss.sheetjs.com/sheetjs/xlsx.full.min.js')
        // document.head.appendChild(recaptchaScript)

    },
    computed:{
        tableData(){
            console.log('dd')
            return this.$store.state.tableData
        },
    }
}
</script>