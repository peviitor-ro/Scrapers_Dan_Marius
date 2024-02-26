# Company ---> promelek
# Link ------> https://promelek.ro/cariere
import re

import unicodedata
from sites.__utils.found_county import get_county
from sites.__utils.dynamic_requests_html_shorts import GetDynamicSoup
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI



def scraper():
    '''
    ... scrape data from imc scraper.
    '''
    
    soup = GetDynamicSoup("https://www.careers-page.com/promelek-xxi")
    job_list = []
    for job in soup.find_all('li', class_="list-group-item row"):
        if job.find('a'):
            link = job.find('a')['href']
            link='https://www.careers-page.com'+link
            description=job.find('span', class_="col").text.strip()
            description_soup=GetDynamicSoup(link)
            location_text=description_soup.find('h5').text.strip()
            town=location_text.split(',')[0]
            judet=get_county(town)
            job_list.append(Item(
                job_title = unicodedata.normalize('NFKD', description).encode('ascii', 'ignore').decode('utf-8'),
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