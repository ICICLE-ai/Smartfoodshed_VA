<template>
    <div>
        <div ref="tabulator">
            <vue-tabulator  ref="tabulator" v-model="dados" :options="options" @dataFiltering="filter" @row-click="onRowClick"/>
        </div>
    </div>
</template>

<script>
import Vue from "vue";
// var Tabulator = require("tabulator-tables");
import vueTabulator from "vue-tabulator";
Vue.use(vueTabulator, { name: "vue-tabulator" });

export default{
    data(){
        return{
            dados:[],
            options: [],
            showTable: false
        }
    },
    created(){
        // this.test()
        this.$store.dispatch('getTableData')
        
    },
    methods:{
        onRowClick(e, row){
            console.log(e,row)
        },
        filter(ele){
            console.log(ele)
        }
    },
    watch:{
        dados(){
            console.log(this.dados)
        },
        tableData(){
            // console.log(this.tableData)
            // this.options= this.tableData['option']
            this.dados = this.tableData['data']
            let temp = {
                'Director': 'Director',
                'Employee': 'Employee',
                'Manager': 'Manager',
                '':'',
                'Member': 'Member',
                'Faculty': 'Faculty',
                'Board Member': 'Board Member',
                'Owner': 'Owner',
                'Advisor': 'Advisor',
                'Student': 'Student'
                }
            var minMaxFilterEditor = function(cell, onRendered, success, cancel, editorParams){
                var end;

                var container = document.createElement("span");

                //create and style inputs
                var start = document.createElement("input");
                start.setAttribute("type", "number");
                start.setAttribute("placeholder", "Min");
                start.setAttribute("min", 0);
                start.setAttribute("max", 100);
                start.style.padding = "4px";
                start.style.width = "50%";
                start.style.boxSizing = "border-box";

                start.value = cell.getValue();

                function buildValues(){
                    success({
                        start:start.value,
                        end:end.value,
                    });
                }

                function keypress(e){
                    if(e.keyCode == 13){
                        buildValues();
                    }

                    if(e.keyCode == 27){
                        cancel();
                    }
                }

                end = start.cloneNode();

                start.addEventListener("change", buildValues);
                start.addEventListener("blur", buildValues);
                start.addEventListener("keydown", keypress);

                end.addEventListener("change", buildValues);
                end.addEventListener("blur", buildValues);
                end.addEventListener("keydown", keypress);


                container.appendChild(start);
                container.appendChild(end);

                return container;
            }
            function minMaxFilterFunction(headerValue, rowValue, rowData, filterParams){
            //headerValue - the value of the header filter element
            //rowValue - the value of the column in this row
            //rowData - the data for the row being filtered
            //filterParams - params object passed to the headerFilterFuncParams property

                if(rowValue){
                    if(headerValue.start != ""){
                        if(headerValue.end != ""){
                            return rowValue >= headerValue.start && rowValue <= headerValue.end;
                        }else{
                            return rowValue >= headerValue.start;
                        }
                    }else{
                        if(headerValue.end != ""){
                            return rowValue <= headerValue.end;
                        }
                    }
                }

    return true; //must return a boolean, true if it passes the filter.
}              

            this.options = {
                'maxHeight': '850px',
                'layout':"fitColumns",
                'responsiveLayout':true, 
                'columns': [{
                    'title': 'Origin',
                    'field': 'Origin County',
                    'headerFilter': 'input'
                },{
                    'title': 'Destination',
                    'field': 'Destination County',
                    'headerFilter': 'input'
                },{
                    'title': 'Weight',
                    'field': 'Weight',
                    'headerFilter':minMaxFilterEditor, 
                    'headerFilterFunc':minMaxFilterFunction
                },{
                    'title': 'Value',
                    'field': 'Value',
                    'headerFilter':minMaxFilterEditor, 
                    'headerFilterFunc':minMaxFilterFunction
                },{
                     'title': 'Travel Distance',
                    'field': 'Travel Distance',
                    'headerFilter':minMaxFilterEditor, 
                    'headerFilterFunc':minMaxFilterFunction
                },{
                    'title': 'Haversine Distance',
                    'field': 'Haversine Distance',
                    'headerFilter':minMaxFilterEditor, 
                    'headerFilterFunc':minMaxFilterFunction
                }]
            }
            this.showTable = true
            // console.log(this.tabulatorInstance)
            // this.tabulatorInstance.modules.filter()
            // this.options = {
            //         'maxHeight': '850px',
            //         'layout':"fitColumns",
            //         'responsiveLayout':true, 
            //         'columns': [
            //             {
            //                 'title': 'Name',
            //                 'field': 'Full Name',
            //                 'headerFilter': 'input'
            //             },{
            //                 'title': 'Organization',
            //                 'field': 'Organization',
            //                 'headerFilter': 'input'
            //             },{
            //                 'title': 'Position',
            //                 'field': 'Position (Verbatim)',
            //                 'headerFilter': 'input'
            //             },{
            //                 'title': 'Position Type',
            //                 'field': 'Position (Type)',
            //                 'editor':"select",
            //                 'editorParams':temp, 
            //                 'headerFilter':true,
            //                 'headerFilterParams':temp,
            //             },{
            //                 'title': 'Start Year',
            //                 'field': 'Year (Start)',
            //                 'headerFilter':minMaxFilterEditor, 
            //                 'headerFilterFunc':minMaxFilterFunction
            //             },{
            //                 'title': 'End Year',
            //                 'field': 'Year (End)',
            //                 'headerFilter':minMaxFilterEditor, 
            //                 'headerFilterFunc':minMaxFilterFunction
            //             }
            //         ]
            //     }
            
        },
        allFilters(){
            console.log(this.allFilters)
        }
    },
    mounted(){
        
        // this.tabulator = new Tabulator(this.$refs.tabulator, {
        //     // data: this.dados, //link data to table
        //     // options: this.options,
        //     dataFiltering:function(filters){
        //     //filters - array of filters currently applied
        //         console.log(filters)
        //     },
        //     // columns: [], //define table columns
        // });
        // let recaptchaScript = document.createElement('script')
        // recaptchaScript.setAttribute('src', 'https://oss.sheetjs.com/sheetjs/xlsx.full.min.js')
        // document.head.appendChild(recaptchaScript)

    },
    computed:{
        tableData(){
            return this.$store.state.tableData
        },
        tabulatorInstance(){
          return this.$refs.tabulator.getInstance()
        },
        allFilters(){
            return this.tabulatorInstance.getFilters(true);
        }
    }
}
</script>