export default {
    state: {
      menuList: [
        {
          label: 'Tabular', //
          icon: 'mdi-table',  
          store: 'documents',
        //   component: () => import('@/components/DocumentsComp')
        }, 
        {
          label: 'Graph view', 
          icon: 'mdi-vector-polygon-variant',
          store: 'graphview',
          component: undefined, 
        }, 
        {
            label: 'Map view', 
            icon: 'mdi-earth-box',
            store: 'ontology',
          //   component: () => import('@/components/GlobalViewComp')
          },
      ]
    }
  }