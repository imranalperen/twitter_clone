<template>
<div class="messages_list_general_container">
    <div class="messages_list_search_box">
        <input id="search_box" type="text" placeholder="Search">
    </div>
    <div class="users_list">
        <div class="user">
            peyami bayram
        </div>
        <div class="user">
            zeliha bayram
        </div>
    </div>
</div>
</template>

<script>
export default {
    props: ["user"]
}

</script>

<style scoped>
.messages_list_general_container {
    display: flex;
    flex-direction: column;
}
.messages_list_search_box {
    background-color: rgba(21, 32, 43, .9);
        display: flex;
    justify-content: center;
}

#search_box {
    background-color: var(--searchbarBG);
    border-style: none;
    padding: .7em;
    font-size: 1em;
    border-radius: 25px;
    margin-top: .3em;
    width: 100%;
    text-indent: 10px;
    outline: none;
    max-width: 350px;
}

::placeholder {
    color: var(--gray);
    font-size: 1em;
    font-weight: 300;
}

#search_box:focus::placeholder {
  color: transparent;
}
</style>