import unicodedata
from __utils.dynamic_requests_html_shorts import GetDynamicSoup
from __utils.found_county import get_county
from __utils.items_struct import Item
from __utils.peviitor_update import UpdateAPI


def scraper():
    '''
    ... scrape data from Gomag scraper.
    '''
    soup = GetDynamicSoup("https://www.gomag.ro/blog/cariere")
    #print (soup)
    job_list = []
    for job in soup.find_all('div', class_="thrv_wrapper thrv_text_element"):
        if job.select('a'):
            job_title=job.find('a').text.strip()
            # job_title= unicodedata.normalize('NFKD', job_title).encode('ascii', 'ignore').decode('utf-8')
            link = job.find('a')['href']
            locations=[]
            if 'Baia Mare' not in job_title and 'Bucuresti' not in job_title:
                locations.append('Baia Mare')
            if 'Baia Mare' in job_title:
                locations.append('Baia Mare')
            if 'Bucuresti' in job_title:
                locations.append('Bucuresti')
            county_list=[]
            for town in locations:
                county=get_county(town)
                if county is not None:  # Check for existing town
                    county_list.append(county)
            if 'remote' in job_title:
                spot='remote'
            else:
                spot='on-site'
            job_list.append(Item(
                job_title = job_title,
                job_link=link,
                company='Gomag',
                country='Romania',
                county=county_list,
                city=locations,
                remote=spot,
            ).to_dict())
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Gomag"
    logo_link = "https://theme.zdassets.com/theme_assets/2161170/a765589a7ac93d2e84133179756f153cd77f4f5e.png"

    jobs = scraper()


    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()