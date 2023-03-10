import { API_URL } from "./localsettings";

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


function delete_tweet_request(tweet_id) {
    const access_token = access_token_control()
    
    let request_body = {
        "tweet_id": tweet_id,
    }
    const fetched_data = fetch(`${API_URL}/delete_tweet`, {
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


function user_profile_image_request(username) {
    const access_token = access_token_control()
    
    let request_body = {
        "target_username": username,
    }
    const fetched_data = fetch(`${API_URL}/user_profile_image`, {
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


function chat_history_request(target_username) {
    const access_token = access_token_control()
    let request_body = {
        "target_username": target_username,
    }
    const fetched_data = fetch(`${API_URL}/chat_history`, {
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

function send_message_request(target_username, message_body) {
    const access_token = access_token_control()
    let request_body = {
        "target_username": target_username,
        "message_body": message_body
    }
    const fetched_data = fetch(`${API_URL}/post_message`, {
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


function chat_contacts_request() {
    const access_token = access_token_control()

    const fetched_data = fetch(`${API_URL}/chat_contacts`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        }
    })
    .then((response) => response.json())

    return fetched_data
}

function get_chat_id_request(target_username) {
    const access_token = access_token_control()
    let request_body = {
        "target_username": target_username,
    }
    const fetched_data = fetch(`${API_URL}/get_chat_id`, {
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

function mark_as_read_message_request(chat_id) {
    const access_token = access_token_control()
    let request_body = {
        "chat_id": chat_id,
    }
    const fetched_data = fetch(`${API_URL}/mark_as_read`, {
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

function last_reply_of_tweet_request(tweet_id) {
    const access_token = access_token_control()
    let request_body = {
        "tweet_id": tweet_id,
    }
    const fetched_data = fetch(`${API_URL}/last_reply_of_user`, {
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


function mark_as_read_notifications_request() {
    const access_token = access_token_control()
   
    const fetched_data = fetch(`${API_URL}/mark_as_read_notifications`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        },
    })
    .then((response) => response.json())

    return fetched_data
}


function notification_count_request() {
    const access_token = access_token_control()
   
    const fetched_data = fetch(`${API_URL}/notification_counts`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        },
    })
    .then((response) => response.json())

    return fetched_data
}

function notifications_request() {
    const access_token = access_token_control()
   
    const fetched_data = fetch(`${API_URL}/notifications`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        },
    })
    .then((response) => response.json())

    return fetched_data
}


function search_users_request(keyword) {
    const access_token = access_token_control()
    let request_body = {
        "keyword": keyword,
    }
    const fetched_data = fetch(`${API_URL}/search_users`, {
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
    user_follows_request,
    verification_code_request,
    reset_password_request,
    update_profile_request,
    delete_tweet_request,
    user_profile_image_request,
    chat_history_request,
    send_message_request,
    chat_contacts_request,
    get_chat_id_request,
    mark_as_read_message_request,
    last_reply_of_tweet_request,
    mark_as_read_notifications_request,
    notification_count_request,
    notifications_request,
    search_users_request
}