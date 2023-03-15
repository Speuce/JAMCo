<!-- eslint-disable no-console -->
<template>
  <v-row>
    <v-dialog v-model="dialog" persistent class="dialog-popup">
      <v-card style="overflow: hidden">
        <v-row class="inner-page-container">
          <v-btn
            @click="this.$emit('close')"
            class=""
            style="position: absolute; top: 35px; left: 25px"
            icon
            flat
          >
            <v-icon size="x-large"> mdi-arrow-left </v-icon>
          </v-btn>
          <v-col class="items">
            <v-row class="center">
              <h2>Add Friends</h2>
            </v-row>
            <v-row style="width: 400px" class="ml-5 pt-5">
              <v-text-field
                v-model="searchField"
                @keyup.enter="triggerSearch"
                placeholder="Search"
                variant="solo"
              >
                <template v-slot:append-inner>
                  <v-btn @click="triggerSearch" icon flat class="mt-n3"
                    ><v-icon>mdi-magnify</v-icon></v-btn
                  >
                </template>
              </v-text-field>
            </v-row>
            <v-row><br /></v-row>
            <div class="scrollable">
              <FriendCard
                class="my-2"
                v-for="user in searchResults"
                :key="user.id"
                :userData="user"
                :isFriend="
                  userData && userData.friends
                    ? userData.friends.some((friend) => friend.id === user.id)
                    : false
                "
                :sentRequest="
                  userData && userData.sent_friend_requests
                    ? userData.sent_friend_requests.includes(user.id)
                    : false
                "
                @sendFriendRequest="sendFriendRequest(user)"
                @removeFriend="removeFriend(user)"
                @viewKanban="viewFriendKanban(user)"
              />
            </div>
            <v-row class="center offset-right">
              <v-col cols="12" sm="6"> </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import FriendCard from './FriendCard.vue'
import { postRequest } from '@/helpers/requests.js'

export default {
  name: 'SearchFriendsModal',
  components: {
    FriendCard,
  },
  emits: ['close', 'fetchUserData'],
  props: {
    userData: {
      type: Object,
      default: undefined,
    },
  },
  data() {
    return {
      dialog: true,
      searchField: '',
      searchResults: [],
    }
  },
  methods: {
    async triggerSearch() {
      const response = await postRequest(
        'account/api/search_users_by_name',
        this.searchField,
      )
      // Filter out the current user from the search results
      this.searchResults = response.user_list.filter(
        (user) => user.id !== this.userData.id,
      )
    },

    async sendFriendRequest(user) {
      await postRequest('account/api/create_friend_request', {
        from_user_id: this.userData.id,
        to_user_id: user.id,
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
    viewFriendKanban(user) {
      // eslint-disable-next-line no-console
      console.log(user)
      // TODO: view friend kanban board
    },
  },
}
</script>

<style scoped>
.inner-page-container {
  padding-top: 3rem;
  padding-left: 6rem;
  padding-bottom: 3rem;
  width: 90%;
}
.offset-right {
  padding-left: 20px;
}
.scrollable {
  overflow-y: auto;
  overflow-x: hidden;
  height: 60vh;
  padding: 20px;
}
.center {
  justify-content: center;
  align-items: center;
}
.dialog-popup {
  max-width: 960px;
}
</style>
