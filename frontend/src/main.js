import { createApp } from 'vue'
import 'vite/modulepreload-polyfill'
import App from './App.vue'
import router from './router'
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader
import './assets/colours.css'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// DatePicker
import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

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
