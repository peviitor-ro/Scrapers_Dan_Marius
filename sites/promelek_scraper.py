# Company ---> promelek
# Link ------> https://promelek.ro/cariere
import re
from __utils import (
    GetDynamicSoup,
    get_county,
    get_job_type,
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
            town=re.search(r'Locație:\s*(.*?)<\/div>', job)
            link=job.find('a')['href']
            judet=get_county(town)
            job_list.append(Item(
                job_title=job.job.find('a').text,
                job_link=link,
                company='imc',
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


    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()