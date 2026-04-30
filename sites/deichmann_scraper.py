import requests

from __utils.found_county import get_county
from __utils.items_struct import Item
from __utils.peviitor_update import UpdateAPI


JOBS_URL = 'https://www.deichmann-cariere.ro/joburi/?&pg=1'
SEARCH_API_URL = 'https://www.deichmann-cariere.ro/wp-admin/admin-ajax.php?action=job_search&count=20&page=1'


def scraper():
    '''
    ... scrape data from Deichmann scraper.
    '''

    response = requests.get(SEARCH_API_URL, timeout=60)
    jobs_data = response.json().get('data', [])
    job_list = []

    for job in jobs_data:
        city = (job.get('city') or '').strip()
        county = get_county(city) if city else None
        link = (job.get('url') or JOBS_URL).replace('//jobs', '/jobs')
        employment_type = (job.get('employment_type') or '').strip().lower()

        if employment_type == 'part time':
            remote = 'part-time'
        elif employment_type == 'full time':
            remote = 'full-time'
        else:
            remote = 'on-site'

        job_list.append(Item(
            job_title=job.get('job_title', '').strip(),
            job_link=link,
            company='Deichmann',
            country='Romania',
            county=county,
            city=city,
            remote=remote,
        ).to_dict())

    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Deichmann"
    logo_link = "https://www.deichmann-cariere.ro/wp-content/themes/karriere/assets/images/deichmann/deichmann.png"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
