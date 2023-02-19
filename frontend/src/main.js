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
  theme: {
    options: {
      customProperties: true,
    },
    defaultTheme: 'jamcoLightTheme',
    themes: {
      jamcoLightTheme: {
        dark: false,
        colors: {
          background: '#FFFFFF',
          surface: '#FFFFFF',
          primary: '#b996ff',
          'primary-darken-1': '#3700B3',
          secondary: '#03DAC6',
          'secondary-darken-1': '#018786',
          error: '#B00020',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FB8C00',
          greyback: '#f7fafc',
          greytext: '#4a5568',
        },
        variables: {},
      },
    },
  },
})

const app = createApp(App).use(vuetify)
app.component('Datepicker', Datepicker)
app.use(router)

app.mount('#app')
