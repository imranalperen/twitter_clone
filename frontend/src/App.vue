<template>
  <div class="router_view_container">
    <router-view
      :current_url="current_url"
      :key="$route.path"
    />
  </div>
</template>


<script>
export default {
  data() {
    return {
      current_url: null
    }
  },

  watch: {
    $route(to, from) {
      this.current_url = to.fullPath.split('/')[1]
    }
  }
}
</script>


<style>
.hashtag_1 {
    font-size: 3em;
    background-color: red;
}

:root {
  --primaryBG: #15202b;
  --secondaryBG: #31404e;
  --gray: #85919e;
  --bordergray:#4F575E;
  --background: #14171A;
  --itemBackground: #d9d9d920;
  --colorWhite: #fff;
  --tweetBtnBg: #1d9bf0;
  --tweetBtnDarkBg: #1a8cd8;
  --grayBlue: #195d8d;
  --whiteHover: #b5b5b5;
  --thirdBG: #1e2732;
  --searchbarBG: #273340;
  --retweet: rgb(85, 188, 133);
  --like: rgb(229, 57, 127);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  color: var(--colorWhite);
}

body {
  background-color: var(--primaryBG);
}
.router_view_container {
  display: flex;
  justify-content: center;
  background-color: var(--primaryBG);
}
</style>
