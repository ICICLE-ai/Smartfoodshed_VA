<template>
    <div id="app">
        <v-app id="inspire">
            <div>
              <v-tabs v-model="tab">
                <v-tab
                  v-for="item in sheetNames"
                  :key="item"
                >
                  {{ item }}
                </v-tab>
              </v-tabs>
             <v-tabs-items v-model="tab">
                <v-tab-item
                  v-for="sheetname in sheetNames"
                  :key="sheetname"
                >
                   <v-data-table
                        v-model="selected_rows"
                        show-select
                        :headers="convert(tableData['data'][sheetname]['tableInfo'])"
                        :items="tableData['data'][sheetname]['tableData']"
                        item-key="name"
                        :single-select="singleSelect"
                        class="elevation-1"
                        :search="search"
                        :custom-filter="filterOnlyCapsText"
                    >
                        <template v-slot:top>
                        <v-text-field
                            v-model="search"
                            label="Search (UPPER CASE ONLY)"
                            class="mx-4"
                        ></v-text-field>
                        </template>
                        <template v-slot:body.append>
                        <tr>
                            <td></td>
                            <td>
                            <v-text-field
                                v-model="calories"
                                type="number"
                                label="Less than"
                            ></v-text-field>
                            </td>
                            <td colspan="4"></td>
                        </tr>
                        </template>
                    </v-data-table>
                </v-tab-item>
              </v-tabs-items>
           
            </div>
        </v-app>
    </div>
</template>

<script>
import {mapState} from 'vuex'
export default{
    data () {
    return {
      search: '',
      calories: '',
      desserts: [],
      headers:[],

      selected_rows:[],
      singleSelect: false,
      sheetNames: [],
      tab: null,
    }
  },
  computed: {
    ...mapState(['tableData', 'tableSelection', 'tableSelected']),
  },
  created(){
    this.$store.dispatch('getTableData')
  },
  methods: {
    filterOnlyCapsText (value, search, item) {
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLocaleUpperCase().indexOf(search) !== -1
    },
    handleSelectionChange (val) {
      // TBA 
      // once change, we save the changes to the global
      this.$store.dispatch('setTableSelected', {sheetName: this.selected_sheet, value: val})

    },
    convert(raw){
      // vuetify need the text + value, not label+value 
      let newOutput = []
      raw.forEach(d=>{
        let temp = {
          text: d['label'],
          value: d['value'],
        }
        newOutput.push(temp)
      })
      return newOutput
    }
  },
  watch:{
     tableData () {
      this.sheetNames = this.tableData['sheet']
    },
  }
}

</script>