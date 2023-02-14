<template>
  <div class="page-container">
    <LoginModalTest v-if="!userData" @signin="userSignedIn" />
    <AccountSetupModal
      v-if="setupModalVisible"
      @updateUser="updateUserAccount"
      :user="this.userData"
    />
    <JobTrackingView :user="this.userData" />
  </div>
</template>

<script>
import LoginModalTest from '@/components/modal/login/LoginModal.vue'
import JobTrackingView from './JobTrackingView.vue'
import AccountSetupModal from '../components/modal/setup/AccountSetupModal.vue'
import { postRequest } from '@/helpers/requests.js'

export default {
  components: {
    LoginModalTest,
    JobTrackingView,
    AccountSetupModal,
  },
  data() {
    return {
      userData: null,
      setupModalVisible: false,
      // TODO grab user data from cookie
    }
  },
  methods: {
    userSignedIn(resp) {
      this.userData = resp.data
      if (resp.created) {
        this.setupModalVisible = true
      }
      // TODO set cookie
    },
    async updateUserAccount(userData) {
      await postRequest('account/api/update_account', userData)
      this.userData = userData
      this.setupModalVisible = false
    },
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
