<template>
  <SearchFriendsModal
    v-if="searchFriendModalVisible"
    @close="searchFriendModalVisible = false"
  />
  <v-row v-if="!searchFriendModalVisible">
    <v-dialog v-model="dialog" persistent class="dialog-popup">
      <v-card style="overflow: hidden">
        <v-row>
          <v-row class="inner-page-container">
            <v-col cols="12" sm="7" class="items">
              <v-row>
                <v-col cols="12" sm="5">
                  <h2>Friends</h2>
                </v-col>
                <v-col cols="12" sm="5">
                  <v-btn
                    class="margin-top"
                    @click="
                      () => {
                        searchFriendModalVisible = true
                      }
                    "
                    >Add Friends<v-divider class="mx-1" /><v-icon
                      >mdi-account-multiple-plus</v-icon
                    ></v-btn
                  >
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-row>
        <RequestCard />
        <FriendCard
          v-for="user in userData.friends"
          :key="user.id"
          :userData="user"
          :isFriend="true"
          @removeFriend="removeFriend(user)"
        />
        <v-card-actions>
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
  padding-top: 2rem;
  padding-left: 3rem;
  padding-bottom: 3rem;
}

.margin-top {
  margin-top: 5px;
}

.dialog-popup {
  max-width: 900px;
}
</style>
