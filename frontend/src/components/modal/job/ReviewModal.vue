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
              hiiiii :D
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
</template>
<script>
export default {
  components: {},

  emits: ['close'],

  props: {},

  data() {
    return {
      dialog: true,
    }
  },
}
</script>
