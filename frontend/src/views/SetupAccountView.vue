<template>
  <div class="center">
    <v-row class="page-container">
      <v-col class="items">
        <v-row class="center">
          <h1>Welcome to JAMCo!</h1>
        </v-row>
        <v-row class="center">
          <h2>Let's finish creating your account.</h2>
        </v-row>
        <v-row> <br /></v-row>
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
  </div>
</template>

<script>
import Datepicker from '@vuepic/vue-datepicker'

export default {
  components: {
    Datepicker,
  },
  data() {
    return {
      firstName: '', // populate from User Object
      lastName: '', // populate from User Object
      birthday: '',
      country: '',
      region: '',
      city: '',
      workField: '',
      firstNameBlank: false,
      lastNameBlank: false,
      countryBlank: false,
      workFieldBlank: false,
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
      if (!this.firstNameBlank && !this.lastNameBlank && !this.countryBlank) {
        // update User Object, redirect to Kanban
      }
    },
  },
}
</script>

<style scoped>
.page-container {
  padding-top: 5rem;
  max-width: 500px;
}
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

#v-text-field label {
  opacity: 0;
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
</style>

<style lang="scss">
$dp__border_radius: 0px !default;
$dp__input_padding: 15px 12px !default;
@import '@vuepic/vue-datepicker/src/VueDatePicker/style/main.scss';
</style>
