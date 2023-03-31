from keys import KeyClass
from retry import Retry
import requests
import time
import hashlib
import logging


def get_flask_api():
    try:
        url = 'http://127.0.0.1:5000/multiply'
        params = {"first_number": "5", "second_number": "5"}
        api_response = requests.get(url, params)
        status_code = api_response.json().get("status_code")
        if status_code == 2001:
            return api_response.json
        elif status_code == 400:
            # the user made a bad request, send the response back notifying them
            return api_response.json
        else:
            # request failed, retry
            backoff_limit = 3
            api_response = Retry().retry_logic(url, backoff_limit, api_response.status_code, params)
            return api_response.json
    except Exception as e:
        logging.error(e)
        return {"status_code": "500"}


def get_marvel_comics():
    try:
        # get the api keys and the current timestamp
        private_key = KeyClass().private_key
        public_key = KeyClass().public_key
        timestamp = get_timestamp()
        # hash the values to authenticate with Marvel's api
        hashed_values = hash_api_keys(private_key, public_key, timestamp)

        # set the parameters and make the api request
        params = {
            "apikey": public_key,
            "ts": timestamp,
            "hash": hashed_values
        }
        url = "http://gateway.marvel.com/v1/public/comics"

        api_response = requests.get(url, params)
        if api_response.status_code == 200:
            return api_response.json()
    except Exception as e:
        logging.error(e)


def hash_api_keys(private_key, public_key, timestamp):
    # hash the api keys and the timestamp to authenticate with Marvel's api
    key_string = timestamp + private_key + public_key
    return hashlib.md5(key_string.encode()).hexdigest()


def get_timestamp():
    # generate a timestamp for the api request
    return str(time.time())


if __name__ == '__main__':
    response = get_flask_api()
    print(response)
