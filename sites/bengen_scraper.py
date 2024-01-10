# New scraper for -> Bengen
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
import re
import json

def get_server_data(link: str):
    '''
    ... this function help me to return fresh data every time.
    return: 
        PHP Session ID,
        CloudFlare ID.
    '''

    response = requests.head(link).headers['Set-Cookie'].split(';')

    php_session_id = ''
    cloudflare_id = ''

    for i in response:
        if 'php' in i.lower():
            php_session_id = i.strip()
        if 'cf' in i.lower():
            cloudflare_id = i.split(',')[-1].strip()

    
    return php_session_id, cloudflare_id

def prepare_headers() -> tuple[str]:
    '''
    prepare headers.
    '''

    # call for ids
    idies = get_server_data('https://bengenro.bamboohr.com/careers/')

    link = 'https://bengenro.bamboohr.com/careers/list'

    headers = {
      'authority': 'bengenro.bamboohr.com',
      'accept': 'application/json, text/plain, */*',
      'cookie': f'{idies[0]}; {idies[1]}',
      'referer': 'https://bengenro.bamboohr.com/careers/',
      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      }

    return link, headers


def get_data():
    '''
    scrape_data.
    '''
    data_from_prepare_headers = prepare_headers()    
    new_response = requests.get(data_from_prepare_headers[0],
                                data_from_prepare_headers[1]).json()
    id_job = re.findall(r'"jobOpeningName": "(.*?)"', json.dumps(new_response))
    id_link = re.findall(r'"id": "(\d+)"', json.dumps(new_response))
    city_data = re.findall(r'"city": "(.*?)"', json.dumps(new_response))
    state_data = re.findall(r'"state": "(.*?)"', json.dumps(new_response))
    #print(id_job, city_data, id_link, state_data)
    list_jobs = []
    for i in range(1, len(id_job) + 1):
        list_jobs.append({
            "job_title": id_job[i-1],
            "job_link": "https://bengenro.bamboohr.com/careers/"+id_link[i-1],
            "company": "bengen",
            "country": "Romania",
            "county": state_data[i-1],
            "city": city_data[i-1],
            "remote":"on-site"
            })
    return list_jobs

#print (get_data())
#
# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'bengen' 
data_list = get_data()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('bengen',
                  'https://bengen.com/wp-content/uploads/2020/04/bengen-logo-svg.svg'
                  ))