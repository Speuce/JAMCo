<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent max-width="900px">
      <v-card>
        <v-card-text>
          <v-row>
            <v-col class="info-col" cols="7">
              <v-select :items="[{}, {}, {}]" label="To:" variant="outlined" />
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
            Cancel
          </v-btn>
          <v-btn color="blue-darken-1" variant="text"> Send </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
export default {
  components: {},
  data() {
    return {
      dialog: true,
    }
  },
}
</script>
