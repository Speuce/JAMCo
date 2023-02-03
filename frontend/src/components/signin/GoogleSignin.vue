<template>
  <div id="signin_button"></div>
</template>
<script>
export default {
  data() {
    return {
      count: 0,
    };
  },
  mounted() {
    window.addEventListener("load", () => {
      window.google.accounts.id.initialize({
        client_id:
          "666407506779-6oo4du8jmenhq8noaa8qkhu89i1ghkpi.apps.googleusercontent.com",
        callback: this.onSignin,
      });
      window.google.accounts.id.renderButton(
        document.getElementById("signin_button"),
        { theme: "outline", size: "large", text: "continue_with", shape: "pill" }
      );
    });
  },

  methods: {
    onSignin(response) {
      console.log(response);
    },
  },
};
</script>
