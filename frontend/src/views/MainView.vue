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
      <LoginModal v-if="!userData && failedAuthentication" @signin="onSignin" />
      <AccountSetupModal
        v-if="setupModalVisible"
        @updateUser="updateUserAccount"
        :user="this.userData"
      />
      <UserInfoModal
        v-if="userInfoModalVisible"
        @updateUser="updateUserAccount"
        :user="this.userData"
        :privacies="this.userPrivacies"
        @close="this.userInfoModalVisible = false"
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
    window.signIn = this.onSignin
    if (token) {
      try {
        await postRequest('account/api/validate_auth_token', token).then(
          (response) => {
            if (response.user) {
              this.userSignedIn({ data: response.user, token: response.token })
            }
          },
        )
      } catch (error) {
        // eslint-disable-next-line no-console
        console.warn('Token Authentication Failed')
      }
    }
    if (!this.userData) this.failedAuthentication = true
  },
  methods: {
    logoutClicked() {
      setAuthToken('')
      location.reload()
    },
    async onSignin(response) {
      const item = {
        credential: response.credential,
        client_id: response.client_id,
      }
      const resp = await postRequest('account/api/get_or_create_account', item)
      this.userSignedIn(resp)
    },
    userSignedIn(resp) {
      this.userData = resp.data
      if (this.setupIncomplete()) {
        this.setupModalVisible = true
      }
      setAuthToken(resp.token)
      this.fetchUserPrivacies()
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
    async fetchUserPrivacies() {
      await postRequest('account/api/get_user_privacies', {
        user_id: this.userData.id,
      }).then((privs) => {
        this.userPrivacies = privs
      })
    },
    async updateUserAccount(userData, userPrivacies) {
      await postRequest('account/api/update_account', userData)

      this.userData = userData

      this.setupModalVisible = false
      this.userInfoModalVisible = false

      // handles case when AccountSetupModal calls updateUserAccount without privacies
      if (userPrivacies) {
        await postRequest('account/api/update_privacies', {
          privacies: userPrivacies,
          user_id: this.userData.id,
        })
        this.userPrivacies = userPrivacies
      }
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
