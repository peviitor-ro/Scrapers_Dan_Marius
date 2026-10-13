#
#
#
# This Decorator will avoid duplicate for me!
# Respect DRY
# This decorator have: default headers and soup and update data on peviitor.ro!
#

import requests
#
import os  # I do not have API KEY
#
import json

from __utils.empty_jobs_repair import (
    NO_JOBS_MARKER,
    clear_cooldown_for_calling_scraper,
    maybe_repair_empty_jobs_output,
)


DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Refer': 'https://google.com',
    'DNT': '1'
}


########### UPDATE API DECORATOR ############
def update_peviitor_api(original_function):
    """
    Decorator for update data on Peviitor.ro API
    """

    def new_function(*args, **kwargs):
        company_name, data_list = args
        #
        validator_endpoint = 'https://api.laurentiumarian.ro/jobs/add/'

        # nu posta o lista goala: ar sterge joburile companiei de pe API
        if not data_list:
            print(f"{company_name} (0 joburi) - nicio pozitie disponibila")
            print(f"Data for {company_name} - no jobs found.")
            # markerul se tipareste inainte de hook: repararea reusita se
            # incheie cu SystemExit(0) si ar suprima orice print de dupa el
            print(f"{NO_JOBS_MARKER} {company_name}", flush=True)
            maybe_repair_empty_jobs_output(company_name)
        else:
            clear_cooldown_for_calling_scraper()
            token = get_token()
            post_header = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }
            res = requests.post(validator_endpoint,
                                json=data_list, headers=post_header)
            print(f"Status code: {res.status_code}")
            print(json.dumps(data_list, indent=4))

        return original_function(*args, **kwargs)

    return new_function


def get_token():
    token_endpoint = 'https://api.laurentiumarian.ro/get_token'
    email = os.environ.get('API_KEY')

    token = requests.post(token_endpoint, json={
        "email": email
    }, headers={
        "Content-Type": "application/json",
    })

    return token.json()['access']
