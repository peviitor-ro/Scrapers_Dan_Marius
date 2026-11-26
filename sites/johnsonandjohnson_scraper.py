import unicodedata
import xml.etree.ElementTree as ET

import requests

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from __utils.found_county import get_county


# careers.jnj.com is protected by a Cloudflare challenge that blocks plain
# requests to its job search pages. The site publishes the same jobs in its
# XML feed, including the country and city needed by the scraper.
BASE_URL = 'https://www.careers.jnj.com'
JOBS_URL = BASE_URL + '/en/jobs/xml/?rss=true'
CITY_COUNTY_OVERRIDES = {
    'Bucuresti': 'Bucuresti',
}


def normalize_city(city):
    normalized_city = ''.join(
        char for char in unicodedata.normalize('NFKD', city.strip())
        if not unicodedata.combining(char)
    )
    if normalized_city == 'Bucuresti':
        return 'Bucuresti'
    return normalized_city


def fetch_job_postings():
    try:
        response = requests.get(JOBS_URL, headers=DEFAULT_HEADERS, timeout=60)
        response.raise_for_status()
        root = ET.fromstring(response.content)
    except (requests.RequestException, ET.ParseError):
        return []

    postings = []
    for job in root.findall('job'):
        postings.append({
            'title': (job.findtext('title') or '').strip(),
            'url': (job.findtext('url') or '').strip(),
            'city': (job.findtext('city') or '').strip(),
            'country': (job.findtext('country') or '').strip(),
        })

    return postings


def collect_data_from_API():
    list_with_data = []

    for job in fetch_job_postings():
        if 'romania' not in job['country'].lower():
            continue

        city = normalize_city(job['city'])
        county = CITY_COUNTY_OVERRIDES.get(city) or get_county(city)

        list_with_data.append({
            'job_title': job['title'],
            'job_link': job['url'],
            'company': 'johnsonandjohnson',
            'country': 'Romania',
            'county': county,
            'city': city,
            'remote': 'on-site'
        })

    return list_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    return data_list


company_name = 'johnsonandjohnson'
data_list = collect_data_from_API()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('johnsonandjohnson',
                  'https://jnj-content-lab2.brightspotcdn.com/ac/25/bd2078f54d5992dd486ed26140ce/johnson-johnson-logo.svg'
                  ))
