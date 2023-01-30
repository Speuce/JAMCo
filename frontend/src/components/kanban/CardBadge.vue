<template>
  <div
    class="px-3 h-6 rounded-full text-xs font-semibold flex items-center"
    v-bind:style="{ backgroundColor: colours[0], color: colours[2] }"
  >
    <span
      class="w-2 h-2 rounded-full mr-1"
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
