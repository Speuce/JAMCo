<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="1200px">
      <v-card>
        <v-card-title>
          <h2 class="mt-3">
            Reviewing
            {{ requestData.sender.first_name }} {{ requestData.sender.last_name }}'s Cover Letter
          </h2>
          <h4>{{ jobData?.position_title }} at {{ jobData?.company }}</h4>
        </v-card-title>
        <v-card-text>
          <div style="display: flex">
            <v-col>
              {{ jobData?.cover_letter }}
            </v-col>
            <v-col>
              <v-textarea
                id="review"
                auto-grow
                class="text-area-box"
                label="Your Review"
                shaped
                v-model="review"
                maxlength="10000"
                variant="outlined"
                rows="3"
              />
            </v-col>
          </div>
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
          <v-btn color="blue-darken-1" variant="text" @click="sendClicked">
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
    request: {
      type: Object,
      default: () => {
        return {
          fulfilled: false,
          id: -1,
          job_id: -1,
          message: '',
          reviewer_id: -1,
          sender_id: -1,
          sender: {
            id: -1,
            first_name: '',
            last_name: '',
            country: '',
          },
        }
      },
    },
  },

  data(props) {
    return {
      dialog: true,
      review: '',
      requestData: props.request,
      jobData: null,
    }
  },

  async mounted() {
    console.log(this.requestData)

    const jobResponse = await postRequest('job/api/get_job_by_id', {
      user_id: this.requestData.sender_id,
      job_id: this.requestData.job_id,
    })

    this.jobData = jobResponse.job_data

    console.log(this.jobData)
  },

  methods: {
    async sendClicked() {
      await postRequest('job/api/create_review', {
        request_id: this.request.id,
        response: this.review,
      })

      this.$emit('close')
    },
  },
}
</script>
