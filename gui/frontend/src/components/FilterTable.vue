<template>
    <div>
        <div>
            <vue-tabulator ref="tabulator" v-model="dados" :options="options"/>
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
            dados:null,
            options: null
        }
    },
    created(){
        this.$store.dispatch('getTableData')
    },
    methods:{

    },
    watch:{
        tableData(){
            this.dados = this.tableData['data']
            this.options= this.tableData['option']
        }
    },
    mounted(){
        // let recaptchaScript = document.createElement('script')
        // recaptchaScript.setAttribute('src', 'https://oss.sheetjs.com/sheetjs/xlsx.full.min.js')
        // document.head.appendChild(recaptchaScript)

    },
    computed:{
        tableData(){
            return this.$store.state.tableData
        },
    }
}
</script>