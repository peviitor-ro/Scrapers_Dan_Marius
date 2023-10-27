##
#
#
# New scraper for -> Compania de Apa Buzau
# Acronis job page -> https://www.cabuzau.ro/despre-noi/cariere/
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
import uuid
#
def collect_data_from_API():
# function to return a list with JSON data
    response=requests.get ('https://www.cabuzau.ro/despre-noi/cariere/', headers=DEFAULT_HEADERS)
    soup=BeautifulSoup(response.text, 'lxml')
    soup_data =soup.find_all('article')
    list_with_data=[]
    for dt in soup_data:
        title=dt.find('h3').text
        link=dt.find('a')['href']
        #
        list_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link": link,
                    "company": "CompaniaDeApaBuzau",
                    "country": "Romania",
                    "city": 'Buzau'
                })
    return list_with_data
#
print(collect_data_from_API())
#
# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'CompaniaDeApaBuzau'  
data_list = collect_data_from_API()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('CompaniaDeApaBuzau',
                  'https://www.cabuzau.ro/wp-content/themes/sst/assets/dist/svg/logo.svg'
                  ))