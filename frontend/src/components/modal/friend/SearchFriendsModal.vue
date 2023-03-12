<template>
  <v-row>
    <v-dialog v-model="dialog" persistent class="dialog-popup">
      <v-card style="overflow: hidden">
        <v-row class="inner-page-container">
          <v-col class="items">
            <v-row class="center">
              <h3>Add Friends</h3>
            </v-row>
            <v-row>
              <v-text-field
                v-model="searchField"
                @keyup.enter="triggerSearch"
              />
              <v-btn @click="triggerSearch" />
            </v-row>
            <v-row><br /></v-row>
            <div class="scrollable">
              <FriendCard
                v-for="user in searchResults"
                :key="user.id"
                :user="user"
                @requestFriend="sendFriendRequest(user)"
              />
            </div>
            <v-row class="center offset-right">
              <v-col cols="12" sm="6">
                <v-btn @click="this.$emit('close')" class=""
                  >Back To Friends</v-btn
                >
              </v-col>
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
  },
  {
    id: 1,
    first_name: 'firstname',
    last_name: 'lastname',
  },
  {
    id: 2,
    first_name: 'f',
    last_name: 'l',
  },
])
export default {
  components: {
    FriendCard,
  },
  emits: ['close'],
  props: {
    user: {
      type: Object,
      default: undefined,
    },
    userFriends: {
      type: Array,
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
  max-width: 700px;
}
</style>
