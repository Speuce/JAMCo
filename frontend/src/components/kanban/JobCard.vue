<template>
  <div class="bg-white shadow rounded px-3 pt-3 pb-5 border border-white">
    <div class="flex justify-between">
      <p class="text-gray-700 font-semibold font-sans tracking-wide text-sm">
        {{ job.company }}
      </p>
      <span class="text-sm text-gray-600">{{ job.date }}</span>
    </div>
    <div class="flex mt-4 justify-between items-center">
      <span class="text-sm text-gray-600" id="job-position">{{
        job.position
      }}</span>
      <CardBadge v-if="job.type" :colours="badgeColours">{{
        job.type
      }}</CardBadge>
    </div>
  </div>
</template>

<script>
import CardBadge from "./CardBadge.vue";
import stringToTriColourPalatte from "../../assets/string-to-tri-colour-palatte";
export default {
  name: "JobCard",
  components: {
    CardBadge,
  },
  props: {
    job: {
      type: Object,
      default: null,
    },
  },
  computed: {
    badgeColours() {
      return stringToTriColourPalatte(this.job.type);
    },
  },
};
</script>
