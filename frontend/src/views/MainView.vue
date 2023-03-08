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
          <v-btn color="primary" flat @click="userInfoModalVisible = true">
            <v-icon size="x-large">mdi-cog</v-icon>
          </v-btn>
        </div>
      </v-col>
    </v-row>
    <div class="page-container flex-grow-1">
      <LoginModal
        v-if="!userData && failedAuthentication"
        @signin="userSignedIn"
      />
      <AccountSetupModal
        v-if="setupModalVisible"
        @updateUser="updateUserAccount"
        :user="this.userData"
      />
      <UserInfoModal
        v-if="userInfoModalVisible"
        @updateUser="updateUserAccount"
        :user="this.userData"
        @close="userInfoModalVisible = false"
        @logout="logoutClicked"
      />
      <Suspense>
        <JobTrackingView
          v-if="this.userData"
          :user="this.userData"
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
import UserInfoModal from '../components/modal/user/UserInfoModal.vue'
import { postRequest } from '@/helpers/requests.js'
import { getAuthToken, setAuthToken } from '@/helpers/auth-cookie.js'

export default {
  components: {
    LoginModal,
    JobTrackingView,
    AccountSetupModal,
    UserInfoModal,
  },
  data() {
    return {
      userData: null,
      userPrivacies: null,
      setupModalVisible: false,
      userInfoModalVisible: false,
      failedAuthentication: false,
    }
  },
  async mounted() {
    let token = getAuthToken()
    if (token) {
      await postRequest('account/api/validate_auth_token', token).then(
        (response) => {
          if (response.user) {
            this.userSignedIn({ data: response.user, token: response.token })
          }
        },
      )
    }
    if (!this.userData) this.failedAuthentication = true
  },
  methods: {
    logoutClicked() {
      setAuthToken('')
      location.reload()
    },
    userSignedIn(resp) {
      this.userData = resp.data
      if (this.setupIncomplete()) {
        this.setupModalVisible = true
      }
      setAuthToken(resp.token)
    },
    setupIncomplete() {
      // check if any req. fields are empty
      return (
        !this.userData.first_name ||
        !this.userData.last_name ||
        !this.userData.email ||
        !this.userData.country ||
        !this.userData.field_of_work
      )
    },
    async updateUserAccount(userData) {
      await postRequest('account/api/update_account', userData)
      this.userData = userData
      this.setupModalVisible = false
      this.userInfoModalVisible = false
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
