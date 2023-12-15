from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import requests
from bs4 import BeautifulSoup
from __utils import get_county
#
def collect_data_from_API():
    custom_headers = {
        "Authority":"jobs.jnj.com",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language":"en-US,en;q=0.5",
        "referer":"https://jobs.jnj.com/en/jobs/?search=USA&pagesize=20",
        "Sec-Fetch-Dest":"document",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-Site":"same-origin",
        "upgrade-insecure-requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
    try:
        response = requests.get("https://jobs.jnj.com/en/jobs/?search=romania&pagesize=20", headers=custom_headers)
        if response.status_code == 200:
            soup=BeautifulSoup(response.text, 'lxml')
            soup_data =soup.find_all('div', class_="card-body")
            list_with_data=[]
            for dt in soup_data:
                title=dt.find('a').text
                link='https://jobs.jnj.com'+dt.find('a')['href']
                location_info=dt.find_all('li')[1]
                location=str(location_info).split(">")[1].split(",")[0]
                if location =='Bucharest':
                    location='Bucuresti'
                judet=get_county(location)
                list_with_data.append({
                    "job_title": title,
                    "job_link": link,
                    "company": "johnsonandjohnson",
                    "country": "Romania",
                    "county": judet,
                    "city": location,
                    "remote": 'on-site'
                    })
            return list_with_data
    except requests.exceptions.RequestException as e:
        print("Error:", e)
#
# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'johnsonandjohnson'  
data_list = collect_data_from_API()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('johnsonandjohnson',
                  'https://jnj-content-lab2.brightspotcdn.com/ac/25/bd2078f54d5992dd486ed26140ce/johnson-johnson-logo.svg'
                  ))