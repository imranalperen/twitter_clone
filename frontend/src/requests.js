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
// function add_tweet_request(request_body) {
//     const access_token = access_token_control()

//     const fetched_data = fetch(`${API_URL}/post_tweet`, {
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
function registration_info_request(profile_image, bio) {
    const access_token = access_token_control()

    const data = new FormData()
    data.append("file", profile_image)
    data.append("bio", bio)
    const fetched_data = fetch(`${API_URL}/registration_info`, {
        method: "POST",
        headers: {
            "access-token": access_token
        },
        body: data
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

function add_replied_tweet_request(tweet_body, image, reply_id) {
    const access_token = access_token_control()

    const data = new FormData()
    data.append("tweet_body", tweet_body)
    data.append("file", image)
    data.append("reply_id", reply_id)
    const fetched_data = fetch(`${API_URL}/add_replied_tweet`, {
        method: "POST",
        headers: {
            "access-token": access_token
        },
        body: data
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

function update_profile_request(profile_image, name, bio) {
    const access_token = access_token_control()
    
    const data = new FormData()
    data.append("file", profile_image)
    data.append("name", name)
    data.append("bio", bio)
    const fetched_data = fetch(`${API_URL}/edit_profile`, {
        method: "POST",
        headers: {
            "access-token": access_token
        },
        body: data
    })
    .then((response) => response.json())

    return fetched_data
}


function add_tweet_request(tweet_body, image) {
    const access_token = access_token_control()

    const data = new FormData()
    data.append("tweet_body", tweet_body)
    data.append("file", image)
    const fetched_data = fetch(`${API_URL}/post_tweet`, {
        method: "POST",
        headers: {
            "access-token": access_token
        },
        body: data
    })
    .then((response) => response.json())

    return fetched_data
}


function user_follows_request(visit_user_id, purpose) {
    const access_token = access_token_control()
    
    let request_body = {
        "visit_user_id": visit_user_id,
        "purpose": purpose
    }
    const fetched_data = fetch(`${API_URL}/follows_and_followers`, {
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

function verification_code_request(mail_adress) {    
    let request_body = {
        "mail_adress": mail_adress
    }
    const fetched_data = fetch(`${API_URL}/send_verify_code `, {
        method: "POST",
        headers: {
            "content-type": "application/json",
        },
        body: JSON.stringify(request_body)
    })
    .then((response) => response.json())

    return fetched_data
}

function reset_password_request(verify_code, password, mail) {
    let request_body = {
        "verify_code": verify_code,
        "password": password,
        "email": mail
    }

    const fetched_data = fetch(`${API_URL}/reset_password`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
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
    user_follows_request,
    verification_code_request,
    reset_password_request,
    update_profile_request,
}