<template>
  <div class="page-container">
    <LoginModalTest v-if="!userData" />
    <JobTrackingView />
  </div>
</template>

<script>
import LoginModalTest from '@/components/modal/login/LoginModal.vue'
import JobTrackingView from './JobTrackingView.vue'

export default {
  components: {
    LoginModalTest,
    JobTrackingView,
  },
  data() {
    return {
      userData: null,
      // TODO grab user data from cookie
    }
  },
}
</script>

<style scoped>
.page-container {
  margin: 1rem 2rem 2rem 2rem;
  min-width: 100vw;
  padding-right: 3.5rem;
  overflow: auto;
}
</style>
