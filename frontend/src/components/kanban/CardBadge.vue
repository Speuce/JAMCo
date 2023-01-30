<template>
  <div
    class="badge-container"
    v-bind:style="{ backgroundColor: colours[0], color: colours[2] }"
  >
    <span
      class="badge-spot"
      v-bind:style="{ backgroundColor: colours[1] }"
    ></span>
    <span>
      <slot></slot>
    </span>
  </div>
</template>

<script>
export default {
  name: "CardBadge",
  props: {
    colours: {
      type: Array,
      default: () => {
        return ["#FFF", "#FFF", "#FFF"];
      },
    },
  },
};
</script>

<style scoped>
.badge-container {
  padding-left: 0.75rem;
  padding-right: 0.75rem;
  height: 1.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.badge-spot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 9999px;
  margin-right: 0.25rem;
}
</style>
