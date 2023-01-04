<template>
  <div class="router_view_container">
    <router-view
      :current_url="current_url"
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
      this.current_url = to.fullPath
    }
  }
}
</script>


<style>
:root {
  --primaryBG: #15202b;
  --secondaryBG: #31404e;
  /* --gray: #707d89; */
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
