<template>
  <div style="height: 100vh" class="d-flex flex-column">
    <v-row class="align-center headerbar ma-0 flex-grow-0">
      <v-col class="py-0"></v-col>
      <v-col class="py-0">
        <v-img
          class="mx-auto"
          src="/static/logo-long.png"
          width="80"
          height="80"
        ></v-img>
      </v-col>
      <v-col class="py-0">
        <div class="text-end">
          <v-btn color="primary" flat @click="settingsVisible = true">
            <v-icon size="x-large">mdi-cog</v-icon>
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <div class="page-container flex-grow-1">
      <LoginModal v-if="!userData" @signin="userSignedIn" />
      <AccountSetupModal
        v-if="setupModalVisible"
        @updateUser="updateUserAccount"
        :user="this.userData"
      />
      <Suspense>
        <JobTrackingView
          v-if="this.userData"
          :user="this.userData"
          :column-modal="columnsModalVisible"
          style="height: 100%"
        />
      </Suspense>
    </div>
  </div>
</template>

<script>
import LoginModal from '@/components/modal/login/LoginModal.vue'
import JobTrackingView from './JobTrackingView.vue'
import AccountSetupModal from '../components/modal/setup/AccountSetupModal.vue'
import { postRequest } from '@/helpers/requests.js'

export default {
  components: {
    LoginModal,
    JobTrackingView,
    AccountSetupModal,
  },
  data() {
    return {
      userData: null,
      setupModalVisible: false,
      // TODO show settings modal
      settingsVisible: false,
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
  min-width: 100vw;
  overflow-y: hidden;
}

.headerbar {
  background-color: var(--vt-c-primary);
  padding: 5px 20px;
}
</style>
