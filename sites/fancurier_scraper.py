import html
import json
import re
import unicodedata

import requests
from bs4 import BeautifulSoup

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from __utils.found_county import get_county


BRANCH_URLS = [
    'https://www.fancourier.ro/cariere/comercial/',
    'https://www.fancourier.ro/cariere/resurse-umane/',
    'https://www.fancourier.ro/cariere/it/',
    'https://www.fancourier.ro/cariere/logistica/',
]
CITY_COUNTY_OVERRIDES = {
    'Bucuresti': 'Bucuresti',
    'Iasi': 'Iasi',
    'Stefanestii de Jos': 'Ilfov',
}


def normalize_text(value):
    return ''.join(
        char for char in unicodedata.normalize('NFKD', value.strip())
        if not unicodedata.combining(char)
    )


def clean_city_name(value):
    city = normalize_text(value)
    city = re.sub(r'\s+', ' ', city)
    city = city.strip(' -,/')
    city = city.replace('Bucuresti Sector 1', 'Bucuresti')
    city = city.replace('Bucuresti Sector 2', 'Bucuresti')
    city = city.replace('Bucuresti Sector 3', 'Bucuresti')
    city = city.replace('Bucuresti Sector 4', 'Bucuresti')
    city = city.replace('Bucuresti Sector 5', 'Bucuresti')
    city = city.replace('Bucuresti Sector 6', 'Bucuresti')
    city = city.replace('Stefanestii De Jos', 'Stefanestii de Jos')
    city = city.replace('Iasi', 'Iasi')
    city = city.replace('Cluj Napoca', 'Cluj-Napoca')
    return city


def extract_title_locations(job_title):
    normalized_title = normalize_text(job_title)
    title_suffix = normalized_title.split('-', 1)
    if len(title_suffix) != 2:
        return []

    location_part = title_suffix[1]
    raw_locations = re.split(r'/|,| si ', location_part)
    title_locations = []
    for raw_location in raw_locations:
        city = clean_city_name(raw_location)
        if not city:
            continue
        if get_county(city) or CITY_COUNTY_OVERRIDES.get(city):
            if city not in title_locations:
                title_locations.append(city)
    return title_locations


def get_job_locations(job):
    title_locations = extract_title_locations(job.get('title', ''))
    if title_locations:
        return title_locations

    locality = clean_city_name(job.get('locality') or '')
    if locality:
        return [locality]

    location = clean_city_name(job.get('location') or '')
    if location and (get_county(location) or CITY_COUNTY_OVERRIDES.get(location)):
        return [location]

    return []


def extract_jobs_from_branch(branch_url):
    response = requests.get(branch_url, headers=DEFAULT_HEADERS, timeout=60)
    soup = BeautifulSoup(response.text, 'lxml')
    data_node = soup.find('div', id='vite-react-division')
    if data_node is None:
        return []

    raw_jobs = data_node.get('data-jobs') or '[]'
    jobs = json.loads(html.unescape(raw_jobs))
    branch_jobs = []

    for job in jobs:
        locations = get_job_locations(job)
        counties = []
        for city in locations:
            county = CITY_COUNTY_OVERRIDES.get(city) or get_county(city)
            if county and county not in counties:
                counties.append(county)

        branch_jobs.append({
            'job_title': job.get('title', '').strip(),
            'job_link': (job.get('link') or '').strip(),
            'company': 'Fancourier',
            'country': 'Romania',
            'county': counties,
            'city': locations,
            'remote': 'on-site',
        })

    return branch_jobs


def collect_data_from_API():
    list_with_data = []
    seen_links = set()

    for branch_url in BRANCH_URLS:
        for job in extract_jobs_from_branch(branch_url):
            job_link = job['job_link']
            if not job_link or job_link in seen_links:
                continue
            seen_links.add(job_link)
            list_with_data.append(job)

    return list_with_data


@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    return data_list


company_name = 'Fancourier'
data_list = collect_data_from_API()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('Fancourier',
                  'https://www.fancourier.ro/wp-content/uploads/2023/03/logo.svg'
                  ))
