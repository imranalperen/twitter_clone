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
        console.log(1)
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

//!like request
function main_user_liked_tweets() {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/main_user_liked_tweets`, {
        method: "GET",
        headers: {
            "content-type": "application/json",
            "access_token": access_token
        },
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
    main_user_liked_tweets,
    unlike_request
}