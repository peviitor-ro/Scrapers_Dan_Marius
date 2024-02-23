# Company ---> rottaprint
# Link ------> https://rottaprint.com/ro/cariere/
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
    
    soup = GetDynamicSoup("https://rottaprint.com/ro/cariere/")
    job_list = []
    for job in soup.find_all('article', class_="job-row post"):
        #get jobs items from response
        oras=job.find('div', attrs={'class': 'job-location'}).text.split(',')[0].strip()
        link=job.find('a')['href']
        judet=get_county(oras)
        job_title=job.find('div', attrs={'class': 'job-title'}).text.strip()
        job_list.append(Item(
            job_title = unicodedata.normalize('NFKD', job_title).encode('ascii', 'ignore').decode('utf-8'),
            job_link=link,
            company='rottaprint',
            country='Romania',
            county=judet,
            city=oras,
            remote='on-site',
        ).to_dict())
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "rottaprint"
    logo_link = "https://rottaprint.com/app/themes/rottaprint/dist/images/logo_b96d8331.svg"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()