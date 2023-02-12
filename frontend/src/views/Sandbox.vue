<template>
  <div class="">
    <h1>This is the login page where you use Google OAuth</h1>
    <GoogleSignin />
  </div>
</template>

<script>
import GoogleSignin from '@/components/signin/GoogleSignin.vue'
export default {
  name: 'LandingView',
  components: {
    GoogleSignin,
  },
  data() {
    return {}
  },

  methods: {},
}
</script>
<style scoped></style>
