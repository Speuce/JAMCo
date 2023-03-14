<!--
TODO:

- Section for Pending Sent Requests
    (RequestCards -> 'sent' list returned from get_user_friend_requests)
- Section for Received Requests awaiting response
    (RequestCards -> 'received' list returned from get_user_friend_requests)
- Section for Current Friends
    (FriendCards -> isFriend prop=true, buttons to view Kanban, remove friend)

-->

<template>
  <SearchFriendsModal
    v-if="searchFriendModalVisible"
    @close="searchFriendModalVisible = false"
  />
  <v-row v-if="!searchFriendModalVisible">
    <v-dialog v-model="dialog" persistent class="dialog-popup">
      <v-card style="overflow: hidden; height: 600px">
        <v-card-title class="inner-page-container">
          <v-row>
            <h2>Friends</h2>
            <v-spacer />
            <v-btn
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
          <div v-if="!userData.friends.length" class="text-center">
            <h3>You Don't have Any Friends! (yet)</h3>
            <p>Click the Add Friends Button at the top to get started</p>
          </div>
          <RequestCard
            v-for="req in requests"
            :key="req.id"
            :request="req"
            :user="userData"
            @acceptRequest="acceptFriendRequest(req)"
            @denyRequest="denyFriendRequest(req)"
          />
          <FriendCard
            v-for="user in userData.friends"
            :key="user.id"
            :userData="user"
            :isFriend="true"
            @removeFriend="removeFriend(user)"
          />
        </div>
        <v-spacer></v-spacer>

        <v-card-actions>
          <v-spacer />
          <v-btn
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

export default {
  name: 'FriendModal',
  components: {
    RequestCard,
    FriendCard,
    SearchFriendsModal,
  },
  emits: ['close'],
  props: {
    userData: {
      type: Object,
      default: () => {
        return {
          id: -1,
          first_name: '',
          last_name: '',
          email: '',
          field_of_work: '',
          country: '',
          region: '',
          city: '',
          birthday: '',
          friends: [],
        }
      },
    },
  },
  data() {
    return {
      dialog: true,
      searchFriendModalVisible: false,
    }
  },
}
</script>

<style scoped>
.inner-page-container {
  padding-top: 40px;
  padding-left: 50px;
  padding-right: 50px;
  padding-bottom: 20px;
}

.margin-top {
  margin-top: 5px;
}

.dialog-popup {
  max-width: 900px;
}
</style>
