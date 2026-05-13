import re

import requests
import unicodedata
from bs4 import BeautifulSoup

from __utils.found_county import get_county
from __utils.items_struct import Item
from __utils.peviitor_update import UpdateAPI

url = "https://altex.ro/cariere/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

def scraper():
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    job_list = []
    for job in soup.find_all('div', class_="border rounded px-8"):
        job_title = job.find('h2').text.strip()
        div_id = re.search(r"<div id=\"([^\"]*)\">", str(job))
        the_id = div_id.group(1)
        link = "https://altex.ro/cariere/#" + the_id
        locations = re.search(r"<!-- --> <!-- -->\s*(.*?)\s*<\/div>", str(job))
        towns = locations.group(1).strip()
        town_list = list(filter(None, map(lambda town: town.strip(), towns.split(","))))
        county_list = []
        for town in town_list:
            county = get_county(town)
            if county is not None:
                county_list.append(county)
        job_list.append(Item(
            job_title=unicodedata.normalize('NFKD', job_title).encode('ascii', 'ignore').decode('utf-8').title(),
            job_link=link,
            company='Altex',
            country='Romania',
            county=county_list,
            city=town_list,
            remote='on-site',
        ).to_dict())
    return job_list


def main():
    company_name = "Altex"
    logo_link = "https://upload.wikimedia.org/wikipedia/ro/thumb/9/9d/Logo_Altex.svg/1200px-Logo_Altex.svg.png"

    jobs = scraper()
    if not jobs:
        return

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
