<template>
  <v-row>
    <v-dialog v-model="dialog" persistent class="dialog-popup">
      <v-card style="overflow: hidden">
        <v-row>
          <v-row class="inner-page-container">
            <v-col cols="12" sm="7" class="items">
              <v-row>
                <v-col cols="12" sm="4">
                  <h2>Settings</h2>
                </v-col>
              </v-row>
              <v-row><br /></v-row>
              <v-row>
                <h3 class="pad-left">Account Info</h3>
              </v-row>
              <v-row><br /></v-row>
              <div class="scrollable">
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
                    :variant="this.editingEnabled ? 'outlined' : 'underlined'"
                    :readonly="!this.editingEnabled"
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
                    :variant="this.editingEnabled ? 'outlined' : 'underlined'"
                    :readonly="!this.editingEnabled"
                  />
                </v-row>
                <v-row>
                  <Datepicker
                    v-if="this.editingEnabled"
                    v-model="this.userData.birthday"
                    :enable-time-picker="false"
                    placeholder="Birthday"
                    class="datepicker"
                    :variant="this.editingEnabled ? 'outlined' : 'underlined'"
                    :readonly="!this.editingEnabled"
                  />
                  <v-text-field
                    v-if="!this.editingEnabled"
                    label="Birthday"
                    required
                    v-model="getBirthdayString"
                    :style="{
                      color: this.lastNameEmpty ? 'red' : '',
                    }"
                    maxlength="30"
                    variant="underlined"
                    readonly
                    :disabled="getBirthdayString == '' && !this.editingEnabled"
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
                    :variant="this.editingEnabled ? 'outlined' : 'underlined'"
                    :readonly="!this.editingEnabled"
                  />
                </v-row>
                <v-row>
                  <v-text-field
                    label="Province/Territory/State"
                    v-model="this.userData.region"
                    maxlength="30"
                    :variant="this.editingEnabled ? 'outlined' : 'underlined'"
                    :readonly="!this.editingEnabled"
                    :disabled="
                      this.userData.region == '' && !this.editingEnabled
                    "
                  />
                </v-row>
                <v-row>
                  <v-text-field
                    label="City"
                    v-model="this.userData.city"
                    maxlength="30"
                    :variant="this.editingEnabled ? 'outlined' : 'underlined'"
                    :readonly="!this.editingEnabled"
                    :disabled="this.userData.city == '' && !this.editingEnabled"
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
                    :variant="this.editingEnabled ? 'outlined' : 'underlined'"
                    :readonly="!this.editingEnabled"
                /></v-row>
                <v-row>
                  <v-text-field
                    label="Email*"
                    v-model="this.userData.email"
                    :style="{ color: this.emailEmpty ? 'red' : '' }"
                    maxlength="30"
                    :variant="this.editingEnabled ? 'outlined' : 'underlined'"
                    :readonly="!this.editingEnabled"
                /></v-row>
              </div>
            </v-col>
            <v-col cols="12" sm="5" class="offset-privacy-col">
              <v-row>
                <h3>Privacy Options</h3>
              </v-row>
            </v-col>
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
                <v-row>
                  <small>* indicates required field</small>
                </v-row>
              </v-col>
            </v-row>
          </v-row>
        </v-row>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="blue-darken-1"
            variant="text"
            @click="
              () => {
                this.editingEnabled = !this.editingEnabled
                if (!this.editingEnabled) {
                  saveChanges()
                }
              }
            "
          >
            <v-icon v-if="this.editingEnabled" left
              >mdi-content-save-outline</v-icon
            >
            <v-icon v-if="!this.editingEnabled" left
              >mdi-square-edit-outline</v-icon
            >
            <v-divider class="mx-1" />
            {{ !this.editingEnabled ? 'Edit' : 'Save' }}
          </v-btn>
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
import Datepicker from '@vuepic/vue-datepicker'

export default {
  components: {
    Datepicker,
  },
  emits: ['close', 'updateUser'],
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
      editingEnabled: false,
      userData: props.user,
    }
  },
  computed: {
    getBirthdayString() {
      return this.userData.birthday !== null
        ? JSON.stringify(this.userData.birthday).substring(1, 11)
        : ''
    },
  },
  methods: {
    saveChanges() {
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
      } else {
        this.editingEnabled = true
      }
    },
  },
}
</script>

<style scoped>
.inner-page-container {
  padding-top: 2rem;
  padding-left: 3rem;
  padding-bottom: 3rem;
}
.offset-right {
  padding-left: 20px;
}
.edit-button {
  margin-top: 5px;
  padding: 0px 10px;
}
.offset-privacy-col {
  padding-top: 105px;
}
.pad-left {
  padding-left: 12px;
}

.scrollable {
  overflow-y: auto;
  overflow-x: hidden;
  height: 50vh;
  padding-left: 12px;
  padding-right: 4rem;
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
  max-width: 900px;
}
</style>

<style lang="scss">
$dp__border_radius: 3px !default;
$dp__input_padding: 15px 12px !default;
@import '@vuepic/vue-datepicker/src/VueDatePicker/style/main.scss';
</style>
