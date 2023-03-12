<template>
  <div></div>
</template>

<!--

<RequestCard
    :request="req"
    @acceptRequest="acceptFriendRequest(req)"
    @denyRequest="denyFriendRequest(req)"
/>

- Show accept & deny options if req.to_user_id === props.user.id
- Show Pending message if req.from_user_id === props.user.id

-->

<script>
export default {
  name: 'RequestCard',
  props: {
    request: {
      type: Object,
      default: undefined,
    },
    user: {
      type: Object,
      default: undefined,
    },
  },
}
</script>

<style scoped></style>
