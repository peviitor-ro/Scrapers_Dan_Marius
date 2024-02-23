# Company ---> hamilton
# Link ------> https://jobs.hamilton.ch/en/open-positions/?country%5B%5D=romania
#
from sites.__utils.dynamic_requests_html_shorts import GetDynamicSoup
from sites.__utils.found_county import get_county
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI

def scraper():
    '''
    ... scrape data from hamilton scraper.
    '''
    soup = GetDynamicSoup("https://jobs.hamilton.ch/en/open-positions/?country%5B%5D=romania")

    job_list = []
    for job in soup.find_all('div', class_='grid-margin job-list__item'):
        title=job.find('a').text
        link=job.find('a')['href']
        location=job.find('span', {'data-ref': 'location'}).text
        oras=location.split(' ')[0].rstrip(",")
        judet=get_county(oras)
        #
        if title and link:
        # get jobs items from response
            job_list.append(Item(
                job_title=title,
                job_link=link,
                company='hamilton',
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

    company_name = "hamilton"
    logo_link = "https://jobs.hamilton.ch/wp-content/themes/dudapress/public/images/hamilton-logo.svg"

    jobs = scraper()

    # uncomment if your scraper done
    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
