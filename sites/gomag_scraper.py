import unicodedata
import re
from __utils.dynamic_requests_html_shorts import GetDynamicSoup
from __utils.found_county import get_county
from __utils.get_job_type import get_job_type
from __utils.items_struct import Item
from __utils.peviitor_update import UpdateAPI


def scraper():
    '''
    ... scrape data from gomag scraper.
    '''
    soup = GetDynamicSoup("https://www.gomag.ro/blog/cariere")
    #print (soup)
    job_list = []
    for job in soup.find_all('div', class_="thrv_wrapper thrv_text_element"):
        print (job)
        # job_title=job.find('h2').text.strip()
        # job_title= unicodedata.normalize('NFKD', job_title).encode('ascii', 'ignore').decode('utf-8')
        # div_id = re.search(r"<div id=\"([^\"]*)\">", str(job))
        # the_id = div_id.group(1)
        # link = "https://altex.ro/cariere/#"+the_id
        # locations=re.search(r"<!-- --> <!-- -->\s*(.*?)\s*<\/div>", str(job))
        # towns=locations.group(1).strip()
        # town_list = list(filter(None, map(lambda town: town.strip(), towns.split(","))))
        # county_list=[]
        # for town in town_list:
        #     county=get_county(town)
        #     if county is not None:  # Check for existing town
        #         county_list.append(county)
        # job_list.append(Item(
        #     job_title = job_title.title(),
        #     job_link=link,
        #     company='Altex',
        #     country='Romania',
        #     county=county_list,
        #     city=town_list,
        #     remote='on-site',
        # ).to_dict())
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "gomag"
    logo_link = "logo_link"

    jobs = scraper()

    # uncomment if your scraper done
    #UpdateAPI().update_jobs(company_name, jobs)
    #UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()