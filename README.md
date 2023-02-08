This is a twitter clone project. My aims of this project are working on a relativly bigger project, coding with a frontend framework (which VueJs) instead of vanilla JS, better understanding for CSS, and implementing of backend external services.

#To Run Localhost
<small>Before starting you need an Ably account (https://ably.com/) and a mailjet account (https://www.mailjet.com/). Both doesn't requieres credit card.</small>

0. clone repo
1. create a database named twitter_clone
2. create a venv in twitter_clone/backend/ activate and
```
pip install -r requirements.txt
```
3. create localsettings.py in twitter_clone/backend/

```
twitter_clone/backend/localsetting.py/


postgresql = {
    "pguser": "YOUR_PGUSER",
    "pgpassword": "YOUR_PG_PASSWORD",
    "pghost": "localhost",
    "pgport": "YOUR PG PORT (DEFAULT 5432)",
    "pgdb": "twitter_clone"
}

MAILJET_SECRET_KEY = "YOUR MAILJET SECRET KEY"
MAILJET_API_KEY = "YOUR MAILJET API KEY"
ABLY_API_KEY = "YOUR ABLY API KEY"
```

backend is ready.


4. twitter_clone/frontend/
```
npm install
```
5. create localsettings.js in twitter_clone/frontend/src/
```
twitter_clone/frontend/src/localsettings.js/

const API_URL = "http://127.0.0.1:5000/api"

const ABLY_API_KEY = "YOUR ABLY API KEY"


export { API_URL, ABLY_API_KEY }
```
frontend is ready.

6. twitter_clone/frontend/
```
npm run serve
```
7. twitter_clone/backend/
you can run in debug mode or
```
FLASK_APP=run.py
flask run
```
