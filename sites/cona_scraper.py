from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from __utils.found_county import get_county
from bs4 import BeautifulSoup
import requests
import unicodedata

CITY_COUNTY_OVERRIDES = {
    'Marsa': 'Sibiu',
    'Selimbar': 'Sibiu',
}


def normalize_text(value):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', value.strip())
        if not unicodedata.combining(c)
    )


def extract_locations(job):
    header = job.find('div', class_='accordion-header')
    location_tag = header.find('p', class_='tag_name', string=lambda text: text and 'Locație:' in text)
    locations = []

    if location_tag:
        raw_locations = location_tag.get_text(' ', strip=True).replace('Locație:', '').split(',')
        for location in raw_locations:
            cleaned_location = normalize_text(location)
            if cleaned_location in {'', 'Hibrid', 'Sediu Central', 'Santier Timisoara'}:
                continue
            if 'Sant' in cleaned_location and 'tara' in cleaned_location.lower():
                continue
            locations.append(cleaned_location)

    body_text = normalize_text(job.get_text(' ', strip=True))
    body_locations = []
    for city in ['Selimbar', 'Marsa', 'Sibiu', 'Bucuresti', 'Timisoara', 'Craiova', 'Huedin', 'Ploiesti']:
        if city in body_text and city not in body_locations:
            body_locations.append(city)

    if body_locations:
        merged_locations = []
        for city in body_locations + locations:
            if city not in merged_locations:
                merged_locations.append(city)
        return merged_locations

    if locations:
        return locations

    return []


def collect_data_from_API():
    response = requests.get('https://cona.ro/cariere/', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    soup_data = soup.find_all('div', class_="accordion-item")
    list_with_data = []
    for dt in soup_data:
        title_tag = dt.find('h3', class_='job_title')
        title = title_tag.get_text(' ', strip=True)
        all_locations = extract_locations(dt)
        county_list = []
        for town in all_locations:
            county = CITY_COUNTY_OVERRIDES.get(town) or get_county(town)
            if county is not None and county not in county_list:
                county_list.append(county)

        list_with_data.append({
            "job_title": title,
            "job_link": f"https://cona.ro/cariere/#{title_tag.get('id')}",
            "company": "Cona",
            "country": "Romania",
            "county": county_list,
            "city": all_locations,
            "remote": 'on-site'
        })
    return list_with_data
# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    return data_list
company_name = 'Cona'
data_list = collect_data_from_API()
scrape_and_update_peviitor(company_name, data_list)
print(update_logo('Cona', 'https://cona.ro/wp-content/uploads/2023/09/cona-logo-1.svg'))
