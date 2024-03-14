# New scraper for -> ONE-IT
import requests
from bs4 import BeautifulSoup

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from sites.__utils.found_county import get_county


#
def collect_data_from_API():
# function to return a list with JSON data
    response=requests.get ('https://www.one-it.ro/cariere/', headers=DEFAULT_HEADERS)
    soup=BeautifulSoup(response.text, 'lxml')
    soup_data = soup.find_all('h2')
    list_with_data=[]
    for dt in soup_data:
        job=dt.find('a', target="_blank")
        if job:
            title=job.text.split(" – ")[0].strip()
            link=dt.find('a')['href']
            all_towns = ["Baia Mare"]
            all_counties=[]
            for town in all_towns:
                county=get_county(town)
                all_counties.append(county)
            list_with_data.append({
                        "job_title": title,
                        "job_link": link,
                        "company": "One-it",
                        "country": "Romania",
                        "county": all_counties,                    
                        "city": all_towns,
                    })
    return list_with_data

# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """
    return data_list


company_name = 'One-it' 
data_list = collect_data_from_API()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('maviprod', 'https://www.one-it.ro/oneitsite/uploads/2019/06/logo_OneIT_255x230px.png'))
