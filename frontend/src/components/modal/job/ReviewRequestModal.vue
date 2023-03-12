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
              <!-- 👇 once friends are in user data: :items="[this.jobData.user.friends]" -->
              <v-select
                item-title="name"
                item-value="id"
                label="Recipient*"
                v-model="selectedFriendId"
                :style="{ color: this.recipientErrorIndicator}"
                variant="outlined"
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
            @click="this.$emit('close')"
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

export default {
  components: {},
  emits: ['close'],
  props: {
    job: {
      type: Object,
      default: () => {
        return {
          user: -1,
          id: -1,
          company: '',
          type: '',
          kcolumn_id: -1,
          position_title: '',
          description: '',
          cover_letter: '',
          notes: '',
        }
      },
    },
  },
  data(props) {
    return {
      dialog: true,
      jobData: props.job,
      selectedFriendId: null,
      message: `Hello, please review my cover letter for ${props.job.position_title} at ${props.job.company}.`,
      messageErrorIndicator: null,
      recipientErrorIndicator: null,
    }
  },
  methods: {
    sendClicked() {
      this.messageErrorIndicator = null

      // TODO: Create review request and POST it
      console.log(this.selectedFriendId)
      console.log(this.message)

      if (this.message /* TODO: && this.recipients or whatever */) {
        this.$emit('close')
      } else if (!this.message) {
        this.messageErrorIndicator = 'red'
      }
    },
  },
}
</script>
<style scoped>
.errorMessage {
  color: red;
}
</style>
