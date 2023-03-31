<template>
  <v-dialog v-model="open" persistent width="400" height="500">
    <v-card style="overflow: hidden" class="px-6 py-4 rounded-lg" height="500">
      <v-col>
        <v-row justify="center" class="mt-6">
          <h2>Welcome toooo</h2>
        </v-row>
        <v-row justify="center">
          <v-img src="/static/logo-long.png" width="200" height="200"></v-img>
        </v-row>
        <v-row justify="center">
          <p class="text-center my-4 mx-4 px-8">
            Sign in to JAMCo to manage and track your job applications
          </p>
        </v-row>
        <v-row justify="center" class="mt-8">
          <div width="200" height="200">
            <GoogleSignin
              @signin="
                (resp) => {
                  $emit('signin', resp)
                }
              "
            />
          </div>
        </v-row>
      </v-col>
    </v-card>
  </v-dialog>
</template>

<script>
import GoogleSignin from '@/components/signin/GoogleSignin.vue'
export default {
  name: 'LoginModal',

  components: {
    GoogleSignin,
  },

  props: {
    value: {
      type: Boolean,
      required: false,
    },
  },
  data() {
    return {
      open: true,
    }
  },
}
</script>
