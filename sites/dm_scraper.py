#
# Company - > dm
# Link -> https://www.dm-jobs.com/Romania/?locale=ro_RO
#
import requests

from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
from found_county import get_county


def get_jobs():
    list_jobs = []

    url = "https://searchui.search.windows.net/indexes/dm-prod/docs/search?api-version=2019-05-06&"

    payload = {
        "count":True,
        "facets":[],
        "filter":"brand eq 'Romania' and isFeatured eq true and datePosted lt 2023-12-03T15:26:41.909Z",
        "search":"*",
        "skip":0,
        "top":9
        }
    headers = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip,deflate,br",
        "Accept-Language":"en-US,en;q=0.5",
        "api-key":"6BBD74F1CBD41E5B0232FB05C5B78ED9",
        "Connection": "keep-alive",
        "Content-Length": "152",
        "Content-Type": "application/json;charset=UTF-8",
        "Host":"searchui.search.windows.net",
        "Origin":"https://www.dm-jobs.com",
        "Referer":"https://www.dm-jobs.com/",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"cross-site",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0"
        }

    response = requests.post(url=url, json=payload, headers=headers).json()['value']

    for job in response:
        title = job['title']
        link = job['link']
        location = job['filter2'].split(" ")[1]
        county = get_county (location)
        list_jobs.append({
            "job_title": title,
            "job_link": link,
            "company": "dm",
            "country": "Romania",
            "county":county,
            "city":location,
            "remote":"on-site"
            })
    return list_jobs
#
# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'dm'
data_list = get_jobs()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('dm',
                  'https://rmkcdn.successfactors.com/92a07e84/2e517b1f-4262-4ee9-bf14-9.png'
                  ))