import requests
from bs4 import BeautifulSoup
import unicodedata

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from __utils.found_county import get_county


JOBS_URL = 'https://www.careers.jnj.com/en/jobs/?search=romania&pagesize=20'
BASE_URL = 'https://www.careers.jnj.com'
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


def collect_data_from_API():
    response = requests.get(JOBS_URL, headers=DEFAULT_HEADERS, timeout=60)
    soup = BeautifulSoup(response.text, 'lxml')
    soup_data = soup.select('ul#js-job-search-results > li.card-job')
    list_with_data = []

    for job in soup_data:
        title_tag = job.select_one('h3.PagePromo-title a.js-view-job')
        location_tag = job.select_one('address.PagePromo-location')
        if title_tag is None or location_tag is None:
            continue

        city = normalize_city(location_tag.get_text(' ', strip=True))
        county = CITY_COUNTY_OVERRIDES.get(city) or get_county(city)
        list_with_data.append({
            'job_title': title_tag.get_text(' ', strip=True),
            'job_link': BASE_URL + title_tag.get('href', '').strip(),
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
