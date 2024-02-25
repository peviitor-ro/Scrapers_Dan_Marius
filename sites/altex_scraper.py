import re

import requests
import unicodedata
from bs4 import BeautifulSoup

from __utils.found_county import get_county
from __utils.items_struct import Item
from __utils.peviitor_update import UpdateAPI

url = "https://altex.ro/cariere/"
headers = {
    'authority': 'altex.ro',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-GB,en;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'bm_sz=9274B37683E6CB64DAE5C359CECA167A~YAAQNmd7XEyTZKqNAQAA+fAhtxb0Lelfe7Lwm9M3cVAiqSgn2kka3i89gQFZxIhXD+bn2vjAUdHbGZr0gU3wbnhr25u7mGkG0hWxvlXpaGIZJaoMDSs3g7orkas7JPFANPVmCUUjh6TP3wv6niX1uC9WxAmdMZOwOFcrhIuczPvz8zck7smeF2uPzuDEC9ngOfIjK0ztQC9IJaVumLVKjdgNt59AfjJBEjrlVb/CSTUeVOs+Gki8Pg86ut1goG1KjQg3Yw4pNCqn2LOmukbLuLSnDIjZLHgV9fuhR8eomwPrIeRLg0AyI7CqXpNCJP9TbVl6cAW3ATqc/OQGUyV7OPAmnwzjK7vNgxD4tI/Q+6mZd7+oT+A=~4337734~4600113; _abck=94E867A19D2FD11EF18CE1917264A211~0~YAAQNmd7XL+TZKqNAQAA8PMhtwsB21DODVV4JD1LZLFYu/9IcZhKgeuG1iMlTjMebpAy/T+34BCn66s6PENaHJcBhoRf+1t53qih85fZn4afmNPJiQ7Wu+RHPd8Fi0wi2VN0G9K2fUCPlT2bDs4MJw/pVWJKAQgI1jFsa9EnX7w7vfzWhguevcjh/n3To0C4Da7pf159CsX5jIGROmo0459MZlpj2lK4tbkTo4tzacAm+DnL2rYX0q8osC5Vxi3hDZgqRIRaNZ9ubu2XHLnB8vVzHD97jbxy6ByBl+wd7YxkTGvqIsb5jvq6d2INRo8nZ9mU99+wTSB7Ss4vS9wDBtCLrY7+3W+rFlP42xS5XYSFDAZoE7lvbi4lyNwsUs6g2Kd8iUOtukCfJgxlgQL2B1zJaBb7sg==~-1~-1~-1',
    'if-none-match': 'W/"9cd4f-/nIWxoN0LL+OxMRPrWF1j2PI3c8"',
    'sec-ch-ua': '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error if HTTP status code is not 200
    #print("Success! Response code:", response.status_code)
    # Parse the HTML content with Beautiful Soup here
    def scraper():
        soup=BeautifulSoup(response.text, 'lxml')
        job_list = []
        for job in soup.find_all('div', class_="border rounded px-8"):
            job_title=job.find('h2').text.strip()
            div_id = re.search(r"<div id=\"([^\"]*)\">", str(job))
            the_id = div_id.group(1)
            link = "https://altex.ro/cariere/#"+the_id
            locations=re.search(r"<!-- --> <!-- -->\s*(.*?)\s*<\/div>", str(job))
            towns=locations.group(1).strip()
            town_list = list(filter(None, map(lambda town: town.strip(), towns.split(","))))
            county_list=[]
            for town in town_list:
                county=get_county(town)
                if county is not None:  # Check for existing town
                    county_list.append(county)
            job_list.append(Item(
                job_title = unicodedata.normalize('NFKD', job_title).encode('ascii', 'ignore').decode('utf-8').title(),
                job_link=link,
                company='Altex',
                country='Romania',
                county=county_list,
                city=town_list,
                remote='on-site',
            ).to_dict())
        return job_list
except requests.exceptions.RequestException as e:
    print("Error:", e)



def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Altex"
    logo_link = "https://upload.wikimedia.org/wikipedia/ro/thumb/9/9d/Logo_Altex.svg/1200px-Logo_Altex.svg.png"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()