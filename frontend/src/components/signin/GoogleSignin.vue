<template>
  <div id="signin_button" style="max-width: 225px"></div>
</template>
<script>
export default {
  data: () => ({}),
  mounted() {
    window.google.accounts.id.initialize({
      client_id:
        '666407506779-6oo4du8jmenhq8noaa8qkhu89i1ghkpi.apps.googleusercontent.com',
      callback: window.signIn,
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

  methods: {},
}
</script>
