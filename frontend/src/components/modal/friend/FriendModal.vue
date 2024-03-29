<template>
  <SearchFriendsModal
    v-if="searchFriendModalVisible"
    @close="searchFriendModalVisible = false"
    :user-data="{ ...userData }"
    @fetchUserData="$emit('fetchUserData', $event)"
    @viewKanban="viewFriend"
  />
  <v-row v-if="!searchFriendModalVisible">
    <v-dialog
      id="friend_modal"
      v-model="dialog"
      persistent
      class="dialog-popup"
    >
      <v-card style="overflow: hidden; height: 600px">
        <v-card-title class="inner-page-container">
          <v-row>
            <h2>Friends</h2>
            <v-spacer />
            <v-btn
              id="add_friends_button"
              color="primary"
              class="margin-top"
              @click="
                () => {
                  searchFriendModalVisible = true
                }
              "
              >Add Friends<v-divider class="mx-1" /><v-icon
                >mdi-account-multiple-plus</v-icon
              >
            </v-btn>
          </v-row>
        </v-card-title>
        <div class="inner-page-container">
          <div
            v-if="
              !userData.friends.length &&
              !userData.received_friend_requests.length
            "
            class="text-center"
          >
            <h3>You Don't have Any Friends! (yet)</h3>
            <p>Click the Add Friends Button at the top to get started</p>
          </div>
          <div v-if="userData.received_friend_requests.length">
            <v-row class="mb-2">
              <v-icon color="grey-darken-1" size="large" class="mr-4"
                >mdi-account-question</v-icon
              >
              <h3>Friend Requests</h3>
            </v-row>

            <div class="scrollable">
              <RequestCard
                v-for="req in userData.received_friend_requests"
                :key="req.id"
                :request="req"
                :user="userData"
                @acceptRequest="acceptFriendRequest(req)"
                @denyRequest="denyFriendRequest(req)"
              />
            </div>
          </div>

          <div>
            <v-row
              class="mb-2 pt-6"
              v-if="
                userData.received_friend_requests.length &&
                userData.friends.length
              "
            >
              <v-icon color="grey-darken-1" size="large" class="mr-4"
                >mdi-account-check</v-icon
              >
              <h3>Friends</h3>
            </v-row>
            <div class="scrollable">
              <FriendCard
                v-for="user in userData.friends"
                :key="user.id"
                :userData="user"
                :isFriend="true"
                @removeFriend="removeFriend(user)"
                @viewKanban="viewFriend(user)"
              />
            </div>
          </div>
        </div>
        <v-spacer></v-spacer>

        <v-card-actions>
          <v-spacer />
          <v-btn
            id="friend_modal_close_button"
            color="blue-darken-1"
            variant="text"
            @click="this.$emit('close')"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import RequestCard from './RequestCard.vue'
import FriendCard from './FriendCard.vue'
import SearchFriendsModal from './SearchFriendsModal.vue'
import { postRequest } from '@/helpers/requests.js'

export default {
  name: 'FriendModal',
  components: {
    RequestCard,
    FriendCard,
    SearchFriendsModal,
  },
  emits: ['close', 'fetchUserData', 'loadFriend'],
  props: {
    userData: {
      type: Object,
      default: undefined,
    },
  },
  data() {
    return {
      dialog: true,
      searchFriendModalVisible: false,
    }
  },
  methods: {
    async acceptFriendRequest(request) {
      await postRequest('account/api/accept_friend_request', {
        request_id: request.id,
        to_user_id: this.userData.id,
        from_user_id: request.from_user_id,
      })
      this.$emit('fetchUserData')
    },
    async denyFriendRequest(request) {
      await postRequest('account/api/deny_friend_request', {
        request_id: request.id,
        from_user_id: request.from_user_id,
        to_user_id: this.userData.id,
      })
      this.$emit('fetchUserData')
    },
    async removeFriend(user) {
      await postRequest('account/api/remove_friend', {
        user1_id: this.userData.id,
        user2_id: user.id,
      })
      this.$emit('fetchUserData')
    },
    viewFriend(user) {
      // set target friend to view and close modal
      this.$emit('loadFriend', user.id)
      this.$emit('close')
    },
  },
}
</script>

<style scoped>
.inner-page-container {
  padding-top: 40px;
  padding-left: 50px;
  padding-right: 50px;
  padding-bottom: 20px;
  overflow-y: auto;
}

.margin-top {
  margin-top: 5px;
}

.dialog-popup {
  max-width: 900px;
}
.scrollable {
  overflow-y: auto;
  overflow-x: hidden;
  max-height: 28vh;
  padding: 1px;
}
</style>
