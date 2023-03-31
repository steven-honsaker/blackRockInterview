import requests
import logging
import time


class Retry:

    def retry_logic(self, url, backoff_limit, status_code, params):
        # default to returning a 500 code and internal server error if something goes wrong
        response = {"status_code": "500", "error_message": "internal server error"}
        # set the time in seconds to progressively backoff request attempts
        request_backoff_time = 2
        logging.error("beginning retry")
        # the number of retry attempts we have made so far
        retry_attempts = 0
        while retry_attempts < backoff_limit and status_code != 2001:
            # attempt request
            logging.error(retry_attempts)
            response = requests.get(url, params)
            # check if we got a 200 status code upon the retry
            if response.status_code == 200:
                logging.info(response.text, response.status_code)
                break
            logging.error(response.text, response.status_code)
            # sleep until the request is allowed to try again
            time.sleep(request_backoff_time)
            # increment the counters
            retry_attempts += 1
            request_backoff_time += 2

        return response
