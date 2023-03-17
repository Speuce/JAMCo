<template>
  <div style="height: 100vh" class="d-flex flex-column">
    <v-row class="align-center headerbar ma-0 flex-grow-0">
      <v-col class="py-0">
        <div class="text-begin">
          <v-btn color="primary" flat @click="returnToHome">
            <v-icon size="x-large" left>mdi-home</v-icon>
            <v-divider class="mx-1" />
            View My Board
          </v-btn>
        </div>
      </v-col>
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
          <v-btn
            v-if="!viewingOther"
            color="primary"
            flat
            @click="showFriendsModal"
          >
            <v-icon size="x-large" left>mdi-account-group</v-icon>
            <v-divider class="mx-1" />
            Friends
          </v-btn>
          <v-btn
            v-if="!viewingOther"
            color="primary"
            flat
            @click="userInfoModalVisible = true"
          >
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
      <FriendModal
        v-if="friendModalVisible"
        :userData="{ ...this.userData }"
        @close="friendModalVisible = false"
        @fetch-user-data="fetchUserData"
        @loadFriend="showFriendKanban"
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
          :key="this.componentKey"
          :user="this.userData"
          :viewingOther="this.viewingOther"
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
import FriendModal from '../components/modal/friend/FriendModal.vue'
import { postRequest } from '@/helpers/requests.js'
import { getAuthToken, setAuthToken } from '@/helpers/auth-cookie.js'

export default {
  components: {
    LoginModal,
    JobTrackingView,
    AccountSetupModal,
    UserInfoModal,
    FriendModal,
  },
  data() {
    return {
      userData: null,
      userPrivacies: null,
      sessionUser: null,
      setupModalVisible: false,
      userInfoModalVisible: false,
      failedAuthentication: false,
      friendModalVisible: false,
      viewingOther: false,
      componentKey: 0,
      authtoken: '',
    }
  },

  async mounted() {
    let token = getAuthToken()
    window.signIn = this.onSignin
    if (token) {
      this.authtoken = token
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
      this.authtoken = ''
      setAuthToken('')
      location.reload()
    },
    async onSignin(response) {
      const item = {
        credential: response.credential,
        client_id: response.client_id,
      }
      this.credential = response.credential
      this.client_id = response.client_id
      const resp = await postRequest('account/api/get_or_create_account', item)

      this.userSignedIn(resp)
    },

    async fetchUserData() {
      if (this.authtoken) {
        const resp = await postRequest(
          'account/api/get_updated_user_data',
          this.authtoken,
        )
        this.userData = resp.user
      } else {
        this.failedAuthentication = true
        this.userData = null
      }
    },

    userSignedIn(resp) {
      this.userData = resp.data
      this.sessionUser = { ...this.userData }
      if (this.setupIncomplete() && !this.viewingOther) {
        this.setupModalVisible = true
      }
      this.authtoken = resp.token
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
      this.sessionUser = { ...this.userData }

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
    showFriendsModal() {
      this.friendModalVisible = true
      this.fetchUserData()
    },
    async showFriendKanban(friendId) {
      // first save the user's info
      this.sessionUser = { ...this.userData }
      // ensure auth'd
      if (this.authtoken) {
        // get friend data
        const resp = await postRequest('account/api/get_friend_data', {
          user_id: this.userData.id,
          friend_id: friendId,
        })
        // toggle view mode and set user data to friend data
        this.viewingOther = true
        // this.userData = resp.friend
        Object.assign(this.userData, resp.friend)
        this.forceRerender()
      } else {
        this.failedAuthentication = true
        this.userData = null
      }
    },
    forceRerender() {
      this.componentKey = !this.componentKey
    },
    returnToHome() {
      this.userData = { ...this.sessionUser }
      this.fetchUserData()
      this.viewingOther = false
      this.forceRerender()
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
