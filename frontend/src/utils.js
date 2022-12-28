import { API_URL } from "./locals";

//! standart user request
function user_request(api_route) {
    const access_token = window.localStorage.getItem("access_token")

    if(!access_token) {
        this.$router.push({name: "login"})
    }

    const fetched_data = fetch(`${API_URL}/${api_route}`, {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "access-token": access_token
        }
    })
    .then((response) => response.json())

    return fetched_data
}

export { user_request }