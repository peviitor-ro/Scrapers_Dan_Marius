import re
import unicodedata

import requests

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from __utils.found_county import get_county


# careers.jnj.com is protected by a Cloudflare challenge that blocks plain
# requests. The site is powered by Workday, so we read the same jobs from its
# public API (the data source behind the careers page).
JOBS_API_URL = 'https://jj.wd5.myworkdayjobs.com/wday/cxs/jj/JJ/jobs'
WORKDAY_BASE_URL = 'https://jj.wd5.myworkdayjobs.com/JJ'
BASE_URL = 'https://www.careers.jnj.com'
SITEMAP_URL = BASE_URL + '/sitemap.xml'
JOB_LINK_PATTERN = re.compile(
    r'<loc>(https://www\.careers\.jnj\.com/en/jobs/([^/<]+)/[^<]*)</loc>'
)
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


def build_job_links():
    job_links = {}
    try:
        response = requests.get(SITEMAP_URL, headers=DEFAULT_HEADERS, timeout=60)
        response.raise_for_status()
    except requests.RequestException:
        return job_links

    for url, job_id in JOB_LINK_PATTERN.findall(response.text):
        job_links[job_id.lower()] = url

    return job_links


def fetch_job_postings():
    postings = []
    offset = 0
    limit = 20

    while True:
        response = requests.post(
            JOBS_API_URL,
            json={
                'appliedFacets': {},
                'limit': limit,
                'offset': offset,
                'searchText': 'romania',
            },
            headers=DEFAULT_HEADERS,
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()

        page = payload.get('jobPostings', [])
        postings.extend(page)

        offset += limit
        if not page or offset >= payload.get('total', len(postings)):
            break

    return postings


def collect_data_from_API():
    job_links = build_job_links()
    list_with_data = []

    for job in fetch_job_postings():
        locations = job.get('locationsText', '')
        if 'romania' not in locations.lower():
            continue

        city = normalize_city(locations.split(',')[0])
        county = CITY_COUNTY_OVERRIDES.get(city) or get_county(city)

        bullet_fields = job.get('bulletFields') or []
        job_id = bullet_fields[0].lower() if bullet_fields else ''
        job_link = job_links.get(job_id) or WORKDAY_BASE_URL + job.get('externalPath', '')

        list_with_data.append({
            'job_title': job.get('title', '').strip(),
            'job_link': job_link,
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
