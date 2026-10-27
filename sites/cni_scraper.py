# New scraper for -> COMPANIA NATIONALA DE INVESTITII
# Careers page -> https://www.cni.ro/noutati/anunturi

import requests
from bs4 import BeautifulSoup

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo


def collect_data_from_API():
    """Return announcements from the current CNI page."""

    headers = {
        **DEFAULT_HEADERS,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    list_with_data = []
    seen_links = set()
    urls = [
        'https://cni.nt.edu.ro/',
        'https://cni.nt.edu.ro/category/noutati/',
        'https://cni.nt.edu.ro/anunt-concurs-posturi-tehnician-informatician/',
    ]

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code >= 400:
                continue
            soup = BeautifulSoup(response.text, 'lxml')
            for anchor in soup.find_all('a', href=True):
                title = anchor.get_text(' ', strip=True)
                link = anchor['href'].strip()
                if not title or not link or link in seen_links:
                    continue
                if 'cariere' not in title.lower() and 'angaj' not in title.lower() and 'concurs' not in title.lower() and 'post' not in title.lower() and 'vacant' not in title.lower() and 'informatic' not in title.lower() and 'tehnician' not in title.lower():
                    continue
                if len(title) < 10:
                    continue

                if link.startswith('/'):
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    base = f'{parsed.scheme}://{parsed.netloc}'
                    link = base + link
                elif not link.startswith('http'):
                    link = url.rstrip('/') + '/' + link

                seen_links.add(link)
                list_with_data.append({
                    "job_title": title,
                    "job_link": link,
                    "company": "CNI",
                    "country": "Romania",
                    "county": 'Neamt',
                    "city": 'Piatra-Neamt',
                    "remote": 'on-site'
                })
        except Exception:
            continue

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
