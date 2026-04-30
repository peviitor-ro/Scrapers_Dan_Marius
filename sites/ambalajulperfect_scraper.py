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
    sections = soup.find_all(
        'section',
        class_=[
            "elementor-section elementor-top-section elementor-element elementor-element-37f35c6 elementor-section-height-min-height elementor-section-boxed elementor-section-height-default elementor-section-items-middle",
            "elementor-section elementor-top-section elementor-element elementor-element-59164de elementor-section-boxed elementor-section-height-default elementor-section-height-default",
        ]
    )
    seen_links = set()

    for section in sections:
        for job in section.find_all('div', class_="elementor-column"):
            link_tag = job.find('a', href=True)
            title_tag = job.find('h5')
            if not link_tag or not title_tag:
                continue

            link = link_tag['href']
            if link in seen_links:
                continue

            seen_links.add(link)
            job_title = title_tag.get_text(' ', strip=True)
            if not job_title:
                widget_container = title_tag.find_parent('div', class_='elementor-widget-container')
                if widget_container:
                    job_title = widget_container.get_text(' ', strip=True)

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
