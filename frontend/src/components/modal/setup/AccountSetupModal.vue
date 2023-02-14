<template>
  <v-row>
    <v-dialog v-model="dialog" persistent class="dialog-popup">
      <v-card style="overflow: hidden">
        <v-row class="inner-page-container">
          <v-col class="items">
            <v-row class="center">
              <h1>Welcome to JAMCo!</h1>
            </v-row>
            <v-row class="center">
              <h2>Let's finish creating your account.</h2>
            </v-row>
            <v-row><br /></v-row>
            <v-row>
              <v-text-field
                label="First Name*"
                required
                v-model="this.userData.first_name"
                :style="{
                  color: this.firstNameEmpty ? 'red' : '',
                }"
                maxlength="30"
                variant="outlined"
              />
            </v-row>
            <v-row>
              <v-text-field
                label="Last Name*"
                required
                v-model="this.userData.last_name"
                :style="{
                  color: this.lastNameEmpty ? 'red' : '',
                }"
                maxlength="30"
                variant="outlined"
              />
            </v-row>
            <v-row>
              <Datepicker
                v-model="this.userData.birthday"
                :enable-time-picker="false"
                placeholder="Birthday"
                class="datepicker"
              />
            </v-row>
            <v-row>
              <v-text-field
                label="Country*"
                v-model="this.userData.country"
                :style="{
                  color: this.countryEmpty ? 'red' : '',
                }"
                maxlength="30"
                variant="outlined"
              />
            </v-row>
            <v-row>
              <v-text-field
                label="Province/Territory/State"
                v-model="this.userData.region"
                maxlength="30"
                variant="outlined"
              />
            </v-row>
            <v-row>
              <v-text-field
                label="City"
                v-model="this.userData.city"
                maxlength="30"
                variant="outlined"
              />
            </v-row>
            <v-row>
              <v-text-field
                label="Field of Work*"
                v-model="this.userData.field_of_work"
                :style="{
                  color: this.workFieldEmpty ? 'red' : '',
                }"
                maxlength="30"
                variant="outlined"
            /></v-row>
            <v-row>
              <v-text-field
                label="Email*"
                v-model="this.userData.email"
                :style="{
                  color: this.emailEmpty ? 'red' : '',
                }"
                maxlength="30"
                variant="outlined"
            /></v-row>
            <v-row class="center">
              <v-col cols="12" sm="8">
                <v-row>
                  <small
                    class="error"
                    v-if="
                      this.firstNameEmpty ||
                      this.lastNameEmpty ||
                      this.emailEmpty ||
                      this.countryEmpty ||
                      this.workFieldEmpty
                    "
                    >Make Sure Required Fields Are Filled</small
                  ></v-row
                >
                <v-row><small>* indicates required field</small></v-row>
              </v-col>
              <v-col cols="12" sm="4">
                <v-btn @click="signUpClicked" class="">Sign Up</v-btn>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import Datepicker from '@vuepic/vue-datepicker'

export default {
  components: {
    Datepicker,
  },
  emits: ['updateUser'],
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
      firstNameEmpty: false,
      lastNameEmpty: false,
      countryEmpty: false,
      workFieldEmpty: false,
      emailEmpty: false,
      userData: props.user,
    }
  },
  methods: {
    signUpClicked() {
      this.firstNameEmpty = false
      this.lastNameEmpty = false
      this.countryEmpty = false
      this.workFieldEmpty = false
      this.emailEmpty = false
      if (!this.userData.first_name || this.userData.first_name.trim() === '') {
        this.firstNameEmpty = true
      }
      if (!this.userData.last_name || this.userData.last_name.trim() === '') {
        this.lastNameEmpty = true
      }
      if (!this.userData.country || this.userData.country.trim() === '') {
        this.countryEmpty = true
      }
      if (
        !this.userData.field_of_work ||
        this.userData.field_of_work.trim() === ''
      ) {
        this.workFieldEmpty = true
      }
      if (!this.userData.email || this.userData.email.trim() === '') {
        this.emailEmpty = true
      }
      if (
        !this.firstNameEmpty &&
        !this.lastNameEmpty &&
        !this.countryEmpty &&
        !this.workFieldEmpty &&
        !this.emailEmpty
      ) {
        this.$emit('updateUser', this.userData)
      }
    },
  },
}
</script>

<style scoped>
.inner-page-container {
  padding-top: 3rem;
  padding-left: 7rem;
  padding-bottom: 3rem;
  width: 90%;
  overflow: hidden;
}
.center {
  justify-content: center;
  align-items: center;
}
.error {
  color: red;
}
.datepicker {
  padding-bottom: 20px;
  --dp-icon-color: #8e8e8e;
  --dp-border-color: #8e8e8e;
  --dp-border-color-hover: #2d2d2d;
  width: 100%;
}
.dialog-popup {
  max-width: 700px;
}
</style>

<style lang="scss">
$dp__border_radius: 3px !default;
$dp__input_padding: 15px 12px !default;
@import '@vuepic/vue-datepicker/src/VueDatePicker/style/main.scss';
</style>
