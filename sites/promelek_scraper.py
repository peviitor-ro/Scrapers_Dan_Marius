# Company ---> promelek
# Link ------> https://promelek.ro/cariere
import re

import unicodedata

from __utils import (
    GetDynamicSoup,
    get_county,
    Item,
    UpdateAPI,
)


def scraper():
    '''
    ... scrape data from imc scraper.
    '''
    
    soup = GetDynamicSoup("https://promelek.ro/cariere")
    job_list = []
    for job in soup.find_all('div', class_="fr-view HtmlBlock_html"):
        #get jobs items from response
        if job.find('a') and (not job.find('div')):
            oras=re.search(r"Locație:\s+(.*)", str(job))
            town=oras.group(1)[:-6]
            link="https://promelek.ro/"+job.find('a')['href']
            judet=get_county(town)
            job_title=job.find('a').text
            job_list.append(Item(
                job_title = unicodedata.normalize('NFKD', job_title).encode('ascii', 'ignore').decode('utf-8'),
                job_link=link,
                company='promelek',
                country='Romania',
                county=judet,
                city=town,
                remote='on-site',
            ).to_dict())
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "promelek"
    logo_link = "https://promelek.ro/content/files/home%20page/plk_logo_mobil_200.png"

    jobs = scraper()



    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()