<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="1200px">
      <v-card>
        <v-card-title>
          <h2 class="mt-3">Reviewing {{ requestData.sender.first_name }}</h2>
        </v-card-title>
        <v-card-text>
          <div style="display: flex">
            <v-col>
              hi
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
            Close
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
    }
  },

  mounted() {
    console.log(this.requestData)
  },
}
</script>
