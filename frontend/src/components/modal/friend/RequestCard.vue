<template>
  <div class="card-container">
    <div class="name-country mt-2">
      <h4>
        {{ request.from_user__first_name }} {{ request.from_user__last_name }}
      </h4>
      <p>, from {{ request.from_user__country }}, wants to be friends.</p>
    </div>
    <div>
      <v-tooltip text="Accept">
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            @click="this.$emit('acceptRequest', request.id)"
            icon
            size="small"
            color="green"
            class="mr-2"
            ><v-icon size="large">mdi-check</v-icon></v-btn
          >
        </template>
      </v-tooltip>
      <v-tooltip text="Deny">
        <template v-slot:activator="{ props }">
          <v-btn
            v-bind="props"
            @click="this.$emit('denyRequest', request.id)"
            icon
            size="small"
            color="red"
          >
            <v-icon size="large"> mdi-close </v-icon>
          </v-btn>
        </template>
      </v-tooltip>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RequestCard',
  props: {
    request: {
      type: Object,
      default: undefined,
    },
  },
  emits: ['acceptRequest', 'denyRequest'],
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
