<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <h2 class="mt-3">Request Cover Letter Review</h2>
          <h5>
            {{ this.jobData.position_title }} at {{ this.jobData.company }}
          </h5>
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col class="info-col" cols="12">
              <v-select
                multiple
                chips
                clearable
                :items="sendableFriends"
                item-title="first_name"
                item-value="id"
                label="Recipients*"
                v-model="selectedFriendIds"
                :style="{ color: this.recipientErrorIndicator }"
                variant="outlined"
                no-data-text="No friends available to review"
              />
            </v-col>
          </v-row>
          <v-row class="mt-n7">
            <v-col cols="12" sm="">
              <v-textarea
                auto-grow
                class="text-area-box"
                label="Message*"
                shaped
                v-model="message"
                :style="{ color: this.messageErrorIndicator }"
                maxlength="10000"
                variant="outlined"
                rows="5"
              />
            </v-col>
          </v-row>
          <h4
            v-if="this.messageErrorIndicator || this.recipientErrorIndicator"
            class="errorMessage"
          >
            Ensure Required (*) Fields Are Filled
          </h4>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="this.closeClicked"
          >
            Cancel
          </v-btn>
          <v-btn color="blue-darken-1" variant="text" @click="sendClicked()">
            Send
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import { postRequest } from '@/helpers/requests.js'

export default {
  components: {},
  emits: ['close'],
  props: {
    job: {
      type: Object,
      default: () => {
        return {
          id: -1,
          company: '',
          type: '',
          kcolumn_id: -1,
          user_id: -1,
          position_title: '',
          description: '',
          cover_letter: '',
          notes: '',
        }
      },
    },
    user: {
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
        }
      },
    },
  },
  data(props) {
    return {
      dialog: true,
      jobData: props.job,
      selectedFriendIds: [],
      message: `Hello, please review my cover letter for ${props.job.position_title} at ${props.job.company}.`,
      messageErrorIndicator: null,
      recipientErrorIndicator: null,
      sendableFriends: [],
    }
  },
  mounted() {
    this.checkSendability()
  },
  methods: {
    sendClicked() {
      this.messageErrorIndicator = null
      this.recipientErrorIndicator = null

      if (this.message.trim() && this.selectedFriendIds.length) {
        this.messageErrorIndicator = null
        this.recipientErrorIndicator = null
        this.$emit('close')
      } else {
        if (!this.message.trim()) {
          this.messageErrorIndicator = 'red'
        }
        if (!this.selectedFriendIds.length) {
          this.recipientErrorIndicator = 'red'
        }
      }
      // only sendable friends were selectable
      this.selectedFriendIds.forEach((friendId) => {
        postRequest('job/api/create_review_request', {
          job_id: this.jobData.id,
          reviewer_id: friendId,
          message: this.message,
        })
      })
    },
    async checkSendability() {
      this.user.friends?.forEach(async (friend) => {
        await postRequest('account/api/get_user_privacies', {
          user_id: friend.id,
        }).then((privs) => {
          if (privs?.cover_letter_requestable) {
            this.sendableFriends.push(friend)
          }
        })
      })
    },
    closeClicked() {
      this.messageErrorIndicator = null
      this.recipientErrorIndicator = null
      this.$emit('close')
    },
  },
}
</script>
<style scoped>
.errorMessage {
  color: red;
}
</style>
