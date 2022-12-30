import { API_URL } from "./locals";

function access_token_control() {
    const access_token = window.localStorage.getItem("access_token")

    if(!access_token) {
        this.$router.push({name: "logn"})
    }
    else {
        return access_token
    }

}

//! standart user request
function timeline_request() {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/timeline`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        }
    })
    .then((response) => response.json())

    return fetched_data
}



//! add tweet request
function add_tweet_request(tweet_body) {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/post_tweet`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token,
            "tweet_body": tweet_body
        }
    })
    .then((response) => response.json())

    return fetched_data
}


//! recommend user request
function recommend_user_request() {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/recommend_follow_user`, {
        methods: "GET",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        }
    })
    .then((response) => response.json())

    return fetched_data
}



export { timeline_request, add_tweet_request, recommend_user_request }