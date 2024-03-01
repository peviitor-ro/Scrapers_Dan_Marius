from sites.__utils.dynamic_requests_html_shorts import GetDynamicSoup
from sites.__utils.found_county import get_county
from sites.__utils.items_struct import Item
from sites.__utils.peviitor_update import UpdateAPI

def scraper():
    '''
    ... scrape data from Deichmann scraper.
    '''
    soup = GetDynamicSoup("https://www.deichmann-cariere.ro/oportunitati-de-angajare/posturi-vacante/")
    #print (soup)
    job_list = []
    for job in soup.find_all('tr', class_="jobs-eintrag parent odd"):
        job_title = job.find_all('a')[0].text
        employment_type = job.find_all('a')[1].text
        link = "https://www.deichmann-cariere.ro/"+job.find('a')['href']
        city = job.find_all('a')[3].text
        county = get_county(city)
        job_list.append(Item(
            job_title = job_title,
            job_link=link,
            company='Deichmann',
            country='Romania',
            county=county,
            city=city,
            remote=employment_type,
        ).to_dict())

    for job in soup.find_all('tr', class_="jobs-eintrag parent even"):
        job_title = job.find_all('a')[0].text
        employment_type = job.find_all('a')[1].text
        link = "https://www.deichmann-cariere.ro/"+job.find('a')['href']
        city = job.find_all('a')[3].text
        county = get_county(city)
        job_list.append(Item(
            job_title = job_title,
            job_link=link,
            company='Deichmann',
            country='Romania',
            county=county,
            city=city,
            remote=employment_type,
        ).to_dict())
    return job_list


def main():
    '''
    ... Main:
    ---> call scraper()
    ---> update_jobs() and update_logo()
    '''

    company_name = "Deichmann"
    logo_link = "https://www.deichmann-cariere.ro/wp-content/themes/karriere/deichmann.svg"

    jobs = scraper()
    print (jobs)

    UpdateAPI().update_jobs(company_name, jobs)
    UpdateAPI().update_logo(company_name, logo_link)


if __name__ == '__main__':
    main()