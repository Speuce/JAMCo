<template>
  <div id="signin_button" style="max-width: 225px"></div>
</template>
<script>
import { postRequest } from '@/helpers/requests.js'
export default {
  data: () => ({}),
  mounted() {
    window.google.accounts.id.initialize({
      client_id:
        '666407506779-6oo4du8jmenhq8noaa8qkhu89i1ghkpi.apps.googleusercontent.com',
      callback: this.onSignin,
    })
    window.google.accounts.id.renderButton(
      document.getElementById('signin_button'),
      {
        theme: 'outline',
        size: 'large',
        text: 'continue_with',
        shape: 'pill',
      },
    )
  },

  methods: {
    async onSignin(response) {
      const item = {
        credential: response.credential,
        client_id: response.client_id,
      }
      const userData = await postRequest(
        'account/api/get_or_create_account',
        item,
      )
      console.log('Userdata: ', userData)
      this.$emit('signin', userData)
    },
  },
}
</script>
