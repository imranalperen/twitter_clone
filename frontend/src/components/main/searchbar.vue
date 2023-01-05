<template>
<div class="main_searchbar">
    <div class="input">
        <input id="searchbar_input" type="text" placeholder="Search Clone" @focus="">
    </div>
</div>
</template>


<script>
export default {
}

</script>


<style scoped>
.main_searchbar {
    padding-bottom: .5em;
    background-color: rgba(21, 32, 43, .9);
}

#searchbar_input {
    background-color: var(--searchbarBG);
    border-style: none;
    padding: .7em;
    font-size: 1em;
    border-radius: 25px;
    margin-top: .3em;
    width: 100%;
    text-indent: 10px;
    outline: none;
}

::placeholder {
    color: var(--gray);
    font-size: 1em;
    font-weight: 300;
}

#searchbar_input:focus::placeholder {
  color: transparent;
}
</style>