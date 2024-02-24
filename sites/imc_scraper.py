# Company ---> imc
# Link ------> https://www.im-c.com/careers/job-offers/
#
from __utils.dynamic_requests_html_shorts import GetDynamicSoup
from __utils.items_struct import Item
from __utils.peviitor_update import UpdateAPI
from __utils.found_county import get_county

def scraper():
    '''
    ... scrape data from imc scraper.
    '''

    soup = GetDynamicSoup("https://www.im-c.com/careers/job-offers/")
    job_list = []
    for job in soup.find_all('li', attrs={'class': 'result result--post_type_job'}):
        # get jobs items from response
        divs=job.find_all('div', class_='result__category')
        town=divs[1].find('div', class_='result__name').text
        judet=get_county(town)
        link=job.find('a')['href']
        if judet:
            job_list.append(Item(
                job_title=job.find('div', class_='result__title').text,
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

    company_name = "imc"
    logo_link = "https://media.licdn.com/dms/image/C4D0BAQHVpmHwmYmvyg/company-logo_200_200/0/1630575054085/imc_ag_logo?e=2147483647&v=beta&t=qOjQCZUEw3jar2giNTB4jXHc5RoplbFkBl6QFeRvU7E"

    jobs = scraper()


    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
