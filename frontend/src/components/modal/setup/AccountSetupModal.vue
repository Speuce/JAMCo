<template>
  <v-row>
    <v-dialog
      v-model="dialog"
      persistent
      class="dialog-popup"
      id="signin_dialog"
    >
      <v-card style="overflow: hidden">
        <v-row class="inner-page-container">
          <v-col class="items">
            <v-row class="center">
              <h1>Welcome to JAMCo!</h1>
            </v-row>
            <v-row class="center">
              <h3>Let's finish creating your account.</h3>
            </v-row>
            <v-row><br /></v-row>
            <div class="scrollable">
              <v-row><br /></v-row>
              <v-row>
                <v-text-field
                  label="First Name*"
                  id="first_name"
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
                  id="last_name"
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
                  id="birthday"
                  v-model="this.userData.birthday"
                  :enable-time-picker="false"
                  placeholder="Birthday"
                  class="datepicker"
                />
              </v-row>
              <v-row>
                <v-text-field
                  label="Country*"
                  id="country"
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
                  id="region"
                  v-model="this.userData.region"
                  maxlength="30"
                  variant="outlined"
                />
              </v-row>
              <v-row>
                <v-text-field
                  label="City"
                  id="city"
                  v-model="this.userData.city"
                  maxlength="30"
                  variant="outlined"
                />
              </v-row>
              <v-row>
                <v-text-field
                  label="Field of Work*"
                  id="field_of_work"
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
                  id="email"
                  v-model="this.userData.email"
                  :style="{
                    color: this.emailEmpty ? 'red' : '',
                  }"
                  maxlength="30"
                  variant="outlined"
              /></v-row>
            </div>
            <v-row class="center offset-right">
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
                <v-btn @click="signUpClicked" class="" id="sign_up_button"
                  >Sign Up</v-btn
                >
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
  padding-left: 6rem;
  padding-bottom: 3rem;
  width: 90%;
}
.offset-right {
  padding-left: 20px;
}

.scrollable {
  overflow-y: auto;
  overflow-x: hidden;
  height: 60vh;
  padding: 20px;
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
  --dp-icon-color: #9f9f9f;
  --dp-border-color: #9f9f9f;
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
