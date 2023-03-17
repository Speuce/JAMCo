<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <h2 class="mt-3">Inbox</h2>
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col>
              <v-row>
                <h3>Review Requests</h3>
              </v-row>
              <v-row
                v-for="request in pendingReviewRequests"
                :key="request.id"
                class="mb-5"
              >
                <div style="display: flex">
                  <v-col cols="9">
                    {{ request.sender.first_name }}
                    {{ request.sender.last_name }}:
                    {{ request.message }}
                  </v-col>
                  <v-col>
                    <v-btn @click="reviewClicked(request)">Review</v-btn>
                  </v-col>
                </div>
              </v-row>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-row>
                <h3>Reviews</h3>
              </v-row>
              <v-row v-for="review in reviews" :key="review.id" class="mb-5">
                <v-col>
                  <v-row>
                    {{ review.reviewer?.first_name }}
                    {{ review.reviewer?.last_name }}
                    reviewed your cover letter for
                    {{ review.job?.position_title }} at
                    {{ review.job?.company }}:
                  </v-row>
                  <v-row>
                    {{ review.response }}
                  </v-row>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card-text>
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
  <div class="page-container flex-grow-1">
    <ReviewModal
      v-if="reviewModalVisible"
      :request="currentlySelectedRequest"
      @close="reviewModalClosed"
    />
  </div>
</template>
<script>
import { postRequest } from '@/helpers/requests.js'
import ReviewModal from './ReviewModal.vue'

export default {
  components: {
    ReviewModal,
  },

  emits: ['close'],

  props: {
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
      reviewModalVisible: false,
      reviewRequests: [],
      reviews: [],
      activeUser: props.user,
      currentlySelectedRequest: null,
    }
  },
  async mounted() {
    const reviewRequestResponse = await postRequest(
      '/job/api/get_review_requests_for_user',
      { user_id: this.user.id },
    )
    this.reviewRequests = reviewRequestResponse.review_requests

    this.reviewRequests.forEach((request) => {
      request.sender = this.activeUser.friends.find(
        (friend) => friend.id === request.sender_id,
      )
    })

    const reviewResponse = await postRequest('/job/api/get_reviews_for_user', {
      user_id: this.user.id,
    })
    this.reviews = reviewResponse.reviews

    this.reviews.forEach(async (review) => {
      const jobResponse = await postRequest('/job/api/get_job_by_id', {
        user_id: this.activeUser.id,
        job_id: review.job_id,
      })
      review.job = jobResponse.job_data

      review.reviewer = this.activeUser.friends.find(
        (friend) => friend.id === review.reviewer_id,
      )
    })
  },

  computed: {
    pendingReviewRequests() {
      console.log(this.reviewRequests)
      return this.reviewRequests.filter((request) => !request.fulfilled)
    },
  },

  methods: {
    reviewClicked(request) {
      this.currentlySelectedRequest = request
      this.reviewModalVisible = true
    },

    async reviewModalClosed() {
      this.reviewModalVisible = false
      const reviewRequestResponse = await postRequest(
        '/job/api/get_review_requests_for_user',
        { user_id: this.user.id },
      )
      const newReviewRequests = reviewRequestResponse.review_requests

      newReviewRequests.forEach((updatedRequest) => {
        const request = this.reviewRequests.find(
          (oldRequest) => oldRequest.id === updatedRequest.id,
        )

        request.fulfilled = updatedRequest.fulfilled
      })
    },
  },
}
</script>

<style scoped>
.scroll-view {
  overflow-y: auto;
  overflow-x: hidden;
  height: 60vh;
  padding: 20px;
}
</style>
