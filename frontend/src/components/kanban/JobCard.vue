<template>
  <div class="card-container">
    <div class="id-company">
      <p class="company">
        {{ job?.company ?? '' }}
      </p>
      <span class="small-gray">{{ job?.id ?? '' }}</span>
    </div>
    <div class="position-container">
      <span class="small-gray" id="job-position">{{
        job?.position ?? ''
      }}</span>
      <CardBadge v-if="job?.type" :colours="badgeColours">{{
        job.type
      }}</CardBadge>
    </div>
  </div>
</template>

<script>
import CardBadge from './CardBadge.vue'
import stringToTriColourPalatte from '../../helpers/string-to-tri-colour-palatte'
export default {
  name: 'JobCard',
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
      return this.job ? stringToTriColourPalatte(this.job.type) : []
    },
  },
}
</script>

<style scoped>
.card-container {
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

.id-company {
  display: flex;
  justify-content: space-between;
}

.company {
  --text-opacity: 1;
  color: #4a5568;
  color: rgba(74, 85, 104, var(--text-opacity));
  font-weight: 600;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji',
    'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji';
  letter-spacing: 0.025em;
  font-size: 0.875rem;
}

.small-gray {
  font-size: 0.875rem;
  --text-opacity: 1;
  color: #718096;
  color: rgba(113, 128, 150, var(--text-opacity));
}

.position-container {
  display: flex;
  margin-top: 1rem;
  justify-content: space-between;
  align-items: center;
}
</style>
