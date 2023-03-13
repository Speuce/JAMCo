<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-card-title>
          <h2 class="mt-3">Cover Letter Review Requests</h2>
        </v-card-title>
        <v-card-text>
          <v-col class="scroll-reviews">
            <v-row
              v-for="request in requestEntries" :key="request.id" class="mb-5"
            >
              <v-col>
                <v-row style="white-space: pre">
                  <b> {{ request.responder }} </b> reviewed your cover letter for
                  <b> {{ request.jobTitle }} </b>
                  at <b> {{ request.company }} </b>:
                </v-row>
                <v-row>
                  {{ request.response }}
                </v-row>
              </v-col>
            </v-row>
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
export default {
  emits: ['close'],
  data() {
    return {
      dialog: true,
      requestEntries: [
        {
          id: 0,
          responder: 'e',
          jobTitle: 'pro gamer',
          company: 'u of m',
          response: 'qwertyuiop',
        },
        {
          id: 1,
          responder: 'f',
          jobTitle: 'pro gamer',
          company: 'u of m',
          response: 'bad',
        },
        {
          id: 2,
          responder: 'g',
          jobTitle: 'pro gamer',
          company: 'u of m',
          response: 'good',
        },
        {
          id: 0,
          responder: 'e',
          jobTitle: 'pro gamer',
          company: 'u of m',
          response: 'qwertyuiop',
        },
        {
          id: 1,
          responder: 'f',
          jobTitle: 'pro gamer',
          company: 'u of m',
          response: 'bad',
        },
        {
          id: 2,
          responder: 'g',
          jobTitle: 'pro gamer',
          company: 'u of m',
          response: 'good',
        },
        {
          id: 0,
          responder: 'e',
          jobTitle: 'pro gamer',
          company: 'u of m',
          response: 'qwertyuiop',
        },
        {
          id: 1,
          responder: 'f',
          jobTitle: 'pro gamer',
          company: 'u of m',
          response: 'bad',
        },
        {
          id: 2,
          responder: 'g',
          jobTitle: 'pro gamer',
          company: 'u of m',
          response: 'good',
        },
        {
          id: 0,
          responder: 'e',
          jobTitle: 'pro gamer',
          company: 'u of m',
          response: 'qwertyuiop',
        },
        {
          id: 1,
          responder: 'f',
          jobTitle: 'pro gamer',
          company: 'u of m',
          response: 'bad',
        },
        {
          id: 2,
          responder: 'g',
          jobTitle: 'pro gamer',
          company: 'u of m',
          response: 'good',
        },
      ],
    }
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
