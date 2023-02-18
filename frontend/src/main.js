import { createApp } from 'vue'
import 'vite/modulepreload-polyfill'
import App from './App.vue'
import router from './router'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import './assets/colours.css'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// DatePicker
import Datepicker from '@vuepic/vue-datepicker'

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
  },
})

const app = createApp(App).use(vuetify)
app.component('Datepicker', Datepicker)
app.use(router)

app.mount('#app')
