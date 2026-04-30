#
# Company - > dm
# Link -> https://www.dm-jobs.ro/job-listing/
#
import requests

from A_OO_get_post_soup_update_dec import update_peviitor_api
from L_00_logo import update_logo
from found_county import get_county


SEARCH_URL = 'https://searchui.search.windows.net/indexes/dm-prod/docs/search?api-version=2019-05-06'
SEARCH_HEADERS = {
    'Accept': '*/*',
    'Content-Type': 'application/json;charset=UTF-8',
    'api-key': '6BBD74F1CBD41E5B0232FB05C5B78ED9',
    'Origin': 'https://www.dm-jobs.ro',
    'Referer': 'https://www.dm-jobs.ro/job-listing/',
    'User-Agent': 'Mozilla/5.0',
}
CITY_COUNTY_OVERRIDES = {
    'Tunari': 'Ilfov',
    'Floresti': 'Cluj',
    'Balotesti': 'Ilfov',
    'Manastirea': 'Dambovita',
    'BUCURESTI SECTOR 1': 'Bucuresti',
}


def fetch_jobs_page(skip=0, top=20):
    payload = {
        'count': True,
        'facets': [],
        'filter': "brand eq 'Romania'",
        'search': '*',
        'skip': skip,
        'top': top,
        'orderby': 'datePosted desc'
    }
    response = requests.post(SEARCH_URL, json=payload, headers=SEARCH_HEADERS, timeout=60)
    return response.json()


def extract_city(job):
    addresses = job.get('addresses') or []
    if addresses:
        first_address = addresses[0]
        return first_address.get('altCity') or first_address.get('city') or ''

    filter_location = (job.get('filter2') or '').strip().split(' ', 1)
    if len(filter_location) == 2:
        return filter_location[1].strip()

    return ''


def get_remote(job):
    work_hours = (job.get('workHours') or '').strip().lower()
    if work_hours == 'part-time':
        return 'part-time'
    if work_hours == 'full time':
        return 'full-time'
    if work_hours == 'full-time':
        return 'full-time'
    return 'on-site'


def get_jobs():
    list_jobs = []
    first_page = fetch_jobs_page()
    total_results = first_page.get('@odata.count', 0)
    jobs = list(first_page.get('value', []))

    for skip in range(len(jobs), total_results, 20):
        jobs.extend(fetch_jobs_page(skip=skip).get('value', []))

    for job in jobs:
        location = extract_city(job)
        county = CITY_COUNTY_OVERRIDES.get(location) or (get_county(location) if location else None)
        list_jobs.append({
            "job_title": job.get('title', '').strip(),
            "job_link": job.get('link', '').strip(),
            "company": "dm",
            "country": "Romania",
            "county": county,
            "city": location,
            "remote": get_remote(job)
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
                  'https://a.storyblok.com/f/290615/97x74/d61d5cd898/dm-logo.svg'
                  ))
