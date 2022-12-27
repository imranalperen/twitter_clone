<template>
  <div class="router_view_container">
    <router-view/>
  </div>
</template>


<script>
export default {
}
</script>


<style>
:root {
  --primaryBG: #15202b;
  --secondaryBG: #31404e;
  --gray: #707d89;
  --background: #14171A;
  --itemBackground: #d9d9d920;
  --colorWhite: #fff;
  --tweetBtnBg: #1d9bf0;
  --tweetBtnDarkBg: #1a8cd8;
  --grayBlue: #195d8d;
  --whiteHover: #b5b5b5;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  color: var(--colorWhite);
}

body {
  background-color: var(--secondaryBG);
}
</style>
