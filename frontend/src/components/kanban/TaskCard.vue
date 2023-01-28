<template>
  <div class="bg-white shadow rounded px-3 pt-3 pb-5 border border-white">
    <div class="flex justify-between">
      <p class="text-gray-700 font-semibold font-sans tracking-wide text-sm">
        {{ task.title }}
      </p>
      <span class="text-sm text-gray-600">{{ task.date }}</span>
    </div>
    <div class="flex mt-4 justify-between items-center">
      <span class="text-sm text-gray-600">{{ task.position }}</span>
      <Badge v-if="task.type" :color="badgeColor">{{ task.type }}</Badge>
    </div>
  </div>
</template>

<script>
import Badge from "./CardBadge.vue";
export default {
  name: "TaskCard",
  components: {
    Badge,
  },
  props: {
    task: {
      type: Object,
      default: () => ({}),
    },
  },
  computed: {
    badgeColor() {
      const mappings = {
        Frontend: "purple",
        "Full Stack": "teal",
        Backend: "blue",
        QA: "green",
        default: "teal",
      };
      return mappings[this.task.type] || mappings.default;
    },
  },
};
</script>
