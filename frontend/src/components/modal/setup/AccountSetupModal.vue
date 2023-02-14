<template>
  <v-row>
    <v-dialog v-model="dialog" persistent class="dialog-popup">
      <v-card class="v-card-background">
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
                v-model="firstName"
                :style="{
                  color: this.firstNameBlank ? 'red' : '',
                }"
                maxlength="30"
                variant="outlined"
              />
            </v-row>
            <v-row>
              <v-text-field
                label="Last Name*"
                required
                v-model="lastName"
                :style="{
                  color: this.lastNameBlank ? 'red' : '',
                }"
                maxlength="30"
                variant="outlined"
              />
            </v-row>
            <v-row>
              <Datepicker
                v-model="birthday"
                :enable-time-picker="false"
                placeholder="Birthday"
                @update:model-value="updateDate"
                class="datepicker"
              />
            </v-row>
            <v-row>
              <v-text-field
                label="Country*"
                v-model="country"
                :style="{
                  color: this.countryBlank ? 'red' : '',
                }"
                maxlength="30"
                variant="outlined"
              />
            </v-row>
            <v-row>
              <v-text-field
                label="Province/Territory/State"
                v-model="region"
                maxlength="30"
                variant="outlined"
              />
            </v-row>
            <v-row>
              <v-text-field
                label="City"
                v-model="city"
                maxlength="30"
                variant="outlined"
              />
            </v-row>
            <v-row>
              <v-text-field
                label="Field of Work*"
                v-model="workField"
                :style="{
                  color: this.workFieldBlank ? 'red' : '',
                }"
                maxlength="30"
                variant="outlined"
            /></v-row>
            <v-row>
              <v-text-field
                label="Email*"
                v-model="email"
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
                    v-if="this.firstNameBlank || this.lastNameBlank"
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
  emits: ['updateUser', 'close'],
  data() {
    return {
      dialog: true,
      firstName: '', // populate from User Object
      lastName: '', // populate from User Object
      birthday: '',
      country: '',
      region: '',
      city: '',
      workField: '',
      email: '',
      firstNameBlank: false,
      lastNameBlank: false,
      countryBlank: false,
      workFieldBlank: false,
      emailEmpty: false,
      userData: {}, // will hold user object
    }
  },
  methods: {
    updateDate(date) {
      this.birthday = date
    },
    signUpClicked() {
      this.firstNameBlank = false
      this.lastNameBlank = false
      this.countryBlank = false
      this.workFieldBlank = false
      this.emailEmpty = false
      if (this.firstName.trim() === '') {
        this.firstNameBlank = true
      }
      if (this.lastName.trim() === '') {
        this.lastNameBlank = true
      }
      if (this.country.trim() === '') {
        this.countryBlank = true
      }
      if (this.workField.trim() === '') {
        this.workFieldBlank = true
      }
      if (this.emailEmpty.trim() === '') {
        this.emailEmpty = true
      }
      if (
        !this.firstNameBlank &&
        !this.lastNameBlank &&
        !this.countryBlank &&
        !this.workFieldBlank &&
        !this.emailEmpty
      ) {
        // update User Object, hide card
        this.$emit('updateUser', this.userData)
        this.$emit('close')
      }
    },
  },
}
</script>

<style scoped>
.inner-page-container {
  padding-top: 3rem;
  padding-left: 7rem;
  padding-bottom: 2rem;
  width: 90%;
}
.center {
  display: flex;
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
  min-height: 1200px;
}
</style>

<style lang="scss">
$dp__border_radius: 0px !default;
$dp__input_padding: 15px 12px !default;
@import '@vuepic/vue-datepicker/src/VueDatePicker/style/main.scss';
</style>
