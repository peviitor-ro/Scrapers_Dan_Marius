# Company ---> Ambalajulperfect
# Link ------> https://ambalajulperfect.ro/cariere/
import unicodedata

from __utils.dynamic_requests_html_shorts import GetDynamicSoup
from __utils.items_struct import Item
from __utils.peviitor_update import UpdateAPI


def scraper():
    '''
    ... scrape data from imc scraper.
    '''

    soup = GetDynamicSoup("https://ambalajulperfect.ro/cariere/")
    job_list = []
    first_soup = soup.find('section',
                           class_="elementor-section elementor-inner-section elementor-element elementor-element-b9cb928 elementor-section-boxed elementor-section-height-default elementor-section-height-default")
    for job in first_soup.find_all('div', class_="elementor-widget-wrap"):
        link = job.find('a')['href']
        job_title = job.find('h5').text.strip()
        job_list.append(Item(
            job_title=unicodedata.normalize('NFKD', job_title).encode('ascii', 'ignore').decode('utf-8'),
            job_link=link,
            company='Ambalajulperfect',
            country='Romania',
            county='Cluj',
            city='Apahida',
            remote='on-site',
        ).to_dict())
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Ambalajulperfect"
    logo_link = "https://ambalajulperfect.ro/wp-content/uploads/2021/11/ap-15-ani-1.png"

    jobs = scraper()

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()
