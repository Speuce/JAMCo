<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <h2 class="mt-3">Cover Letter Review Requests</h2>
        </v-card-title>
        <v-card-text>
          <v-col v-if="requestEntries.length > 0" class="scroll-reviews">
            <v-row
              v-for="request in requestEntries"
              :key="request.id"
              class="mb-5"
            >
              <v-col>
                <v-row style="white-space: pre">
                  <b> {{ request.responder }} </b> reviewed your cover letter
                  for <b> {{ request.jobTitle }} </b> at
                  <b> {{ request.company }} </b>:
                </v-row>
                <v-row>
                  {{ request.response }}
                </v-row>
              </v-col>
            </v-row>
          </v-col>
          <v-col v-else>
            You have no incoming cover letter reviews or review requests. You can ask your friends
            to review your cover letters by pressing the "Request Review" button
            next to any cover letter.
          </v-col>
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
</template>
<script>
import { postRequest } from '@/helpers/requests.js'

export default {
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
      requestEntries: [],
      activeUser: props.user,
    }
  },
  async mounted() {
    console.log(this.requestEntries)
    console.log(Boolean(this.requestEntries.length))

    const reviews = await postRequest('/job/api/get_reviews_for_user', {
      user_id: this.user.id,
    })

    console.log(reviews)
  },
}
</script>

<style scoped>
.scroll-reviews {
  overflow-y: auto;
  overflow-x: hidden;
  height: 60vh;
  padding: 20px;
}
</style>
