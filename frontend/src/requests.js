import { API_URL } from "./locals";


//!signup request
function signup_request(request_body) {
    const fetched_data = fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}


//!login request
function login_request(request_body) {
    const fetched_data = fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}


function access_token_control() {
    const access_token = window.localStorage.getItem("access_token")

    if(!access_token) {
        window.localStorage.clear()
        location.href = 'http://localhost:8080/login'
    }
    else {
        return access_token
    }
}

//! standart user request
function user_request() {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/user`, {
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
function add_tweet_request(request_body) {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/post_tweet`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        },
        body: JSON.stringify(request_body)
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
    .then((response_value) => response_value.response)

    return fetched_data
}


//! follow user request
function follow_request(user_id) {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/follow_user`, {
        methods: "GET",
        headers: {
            "content-type": "application/json",
            "access-token": access_token,
            "user-id": user_id
        }
    })
    .then((response) => response.json())

    return fetched_data
}


//! unfollow user request
function unfollow_request(user_id) {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/unfollow_user`, {
        methods: "GET",
        headers: {
            "content-type": "application/json",
            "access-token": access_token,
            "user-id": user_id
        }
    })
    .then((response) => response.json())

    return fetched_data
}

//! timeline request
function timeline_request() {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/timeline`, {
        methods: "GET",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        }
    })
    .then((response) => response.json())

    return fetched_data
}

//! registration_info_request
function registration_info_request(request_body) {
    const access_token = access_token_control()
    const fetched_data = fetch(`${API_URL}/registration_info`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "access-token": access_token
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}

//!like request
function like_request(request_body) {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/like_tweet`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access_token": access_token
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}

function unlike_request(request_body) {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/unlike_tweet`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access_token": access_token
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}

function retweet_request(request_body) {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/retweet`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access_token": access_token
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}

function unretweet_request(request_body) {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/unretweet`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access_token": access_token
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}

function last_tweet_of_user_request() {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/user_last_tweet`, {
        method: "GET",
        headers: {
            "content-type": "application/json",
            "access_token": access_token
        },
    })
    .then((response) => response.json())

    return fetched_data
}

function add_replied_tweet_request(request_body) {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/add_replied_tweet`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}

function tweet_page_request(request_body) {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/tweet_page`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}

function trend_topics_request() {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/trend_topics`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access_token": access_token
        },
    })
    .then((response) => response.json())


    return fetched_data
}


function topic_request(topic) {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/trend/${topic}`, {
        headers: {
            "content-type": "application/json",
            "access_token": access_token
        },
    })
    .then((response) => response.json())

    return fetched_data
}


function explore_timeline_request() {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/explore`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access_token": access_token
        },
    })
    .then((response) => response.json())


    return fetched_data
}

function profile_request(username) {
    const access_token = access_token_control()

    let request_body = {
        "username": username
    }

    const fetched_data = fetch(`${API_URL}/profile`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}


// function profile_tweets_request(username) {
//     const access_token = access_token_control()

//     let request_body = {
//         "username": username
//     }

//     const fetched_data = fetch(`${API_URL}/profile_tweets`, {
//         method: "POST",
//         headers: {
//             "content-type": "application/json",
//             "access-token": access_token
//         },
//         body: JSON.stringify(request_body)
//     })
//     .then((response) => response.json())

//     return fetched_data
// }

function profile_media_request(username) {
    const access_token = access_token_control()

    let request_body = {
        "username": username
    }

    const fetched_data = fetch(`${API_URL}/profile_media`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}

function profile_tweets_request(username, profile_tab) {
    const access_token = access_token_control()

    let request_body = {
        "username": username,
        "profile_tab": profile_tab
    }

    const fetched_data = fetch(`${API_URL}/profile_feed`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}


export {
    signup_request,
    login_request,
    user_request,
    add_tweet_request,
    recommend_user_request,
    follow_request,
    unfollow_request,
    timeline_request,
    registration_info_request,
    like_request,
    unlike_request,
    retweet_request,
    unretweet_request,
    last_tweet_of_user_request,
    add_replied_tweet_request,
    tweet_page_request,
    trend_topics_request,
    topic_request,
    explore_timeline_request,
    profile_request,
    profile_tweets_request,
    profile_media_request,
}