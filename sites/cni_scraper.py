# New scraper for -> COMPANIA NATIONALA DE INVESTITII
# Careers page -> https://www.cni.ro/noutati/anunturi

import requests
from bs4 import BeautifulSoup

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo


def collect_data_from_API():
    """Return announcements from the current CNI page."""

    response = requests.get('https://www.cni.ro/noutati/anunturi', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    list_with_data = []
    seen_links = set()

    for anchor in soup.find_all('a', href=True):
        title_tag = anchor.find('h2')
        if not title_tag:
            continue

        title = title_tag.get_text(' ', strip=True)
        link = anchor['href'].strip()
        if not title or not link or link in seen_links:
            continue

        seen_links.add(link)
        list_with_data.append({
            "job_title": title,
            "job_link": link,
            "company": "CNI",
            "country": "Romania",
            "county": 'Bucuresti',
            "city": 'Bucuresti',
            "remote": 'on-site'
        })

    return list_with_data


# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'CNI'
data_list = collect_data_from_API()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('CNI',
                  'https://www.cni.ro/cni.jpg'
                  ))
