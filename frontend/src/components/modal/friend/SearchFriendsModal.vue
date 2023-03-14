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
                    ? userData.friends.contains(user.id)
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
import { ref } from 'vue'

// Demo Results for testing FriendCard
const searchResults = ref([
  {
    id: 0,
    first_name: 'first',
    last_name: 'last',
    country: 'CA',
  },
  {
    id: 1,
    first_name: 'firstname',
    last_name: 'lastname',
    country: 'CA',
  },
  {
    id: 2,
    first_name: 'f',
    last_name: 'l',
    country: 'US',
  },
])
export default {
  name: 'SearchFriendsModal',
  components: {
    FriendCard,
  },
  emits: ['close'],
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
      searchResults,
    }
  },
  methods: {
    triggerSearch() {
      // eslint-disable-next-line no-console
      console.log('search: ' + this.searchField)
    },
    sendFriendRequest(user) {
      // eslint-disable-next-line no-console
      console.log(user)
      // TODO: send friend request to user
    },
    removeFriend(user) {
      // eslint-disable-next-line no-console
      console.log(user)
      // TODO: remove friend from user
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
