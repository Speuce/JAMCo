<template>
  <div class="card-container">
    <div class="name-country">
      <h4>{{ userData.first_name }} {{ userData.last_name }}</h4>
      <p>, {{ userData.country }}</p>
    </div>
    <div>
      <v-tooltip text="Add Friend">
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            v-if="!isFriend && !sentRequest"
            @click="this.$emit('sendFriendRequest', userData.id)"
            icon
            size="small"
            color="primary"
            ><v-icon size="large">mdi-account-plus</v-icon></v-btn
          >
        </template>
      </v-tooltip>
      <v-tooltip text="Pending Friend Request">
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            v-if="!isFriend && sentRequest"
            disabled
            icon
            size="small"
            color="primary"
            ><v-icon size="large">mdi-check</v-icon></v-btn
          >
        </template>
      </v-tooltip>
      <v-tooltip text="View Kanban">
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            v-if="isFriend"
            @click="this.$emit('viewKanban', userData.id)"
            icon
            size="small"
            color="secondary"
          >
            <v-icon size="large"> mdi-view-dashboard-variant-outline </v-icon>
          </v-btn>
        </template>
      </v-tooltip>
      <v-tooltip text="Remove Friend">
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            v-if="isFriend"
            @click="this.$emit('removeFriend', userData.id)"
            icon
            size="small"
            color="red"
          >
            <v-icon>mdi-trash-can-outline</v-icon>
          </v-btn>
        </template>
      </v-tooltip>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FriendCard',
  emits: ['viewKanban', 'removeFriend', 'sendFriendRequest'],
  props: {
    userData: {
      type: Object,
      default: () => {
        return {
          id: -1,
          first_name: 'first',
          last_name: 'last',
          country: 'CA',
        }
      },
    },
    isFriend: {
      type: Boolean,
      default: false,
    },
    sentRequest: {
      type: Boolean,
      default: false,
    },
  },
}
</script>

<style scoped>
.card-container {
  display: flex;
  justify-content: space-between;
  --bg-opacity: 1;
  background-color: #fff;
  background-color: rgba(255, 255, 255, var(--bg-opacity));
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  border-radius: 0.25rem;
  padding: 0.75rem;
  border-width: 1px;
  --border-opacity: 1;
  border-color: rgba(255, 255, 255, var(--border-opacity));
}

.name-country {
  display: flex;
}
</style>