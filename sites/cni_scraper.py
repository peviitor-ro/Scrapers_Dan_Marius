##
#
#
# New scraper for -> COMPANIA NATIONALA DE INVESTITII
# Acronis job page -> https://www.cni.ro/despre-noi#
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
import uuid
#
def collect_data_from_API():
# function to return a list with JSON data
    response=requests.get ('https://www.cni.ro/despre-noi#', headers=DEFAULT_HEADERS)
    soup=BeautifulSoup(response.text, 'lxml')
    soup_data =soup.find('div', id="item4")
    soup_data_final= soup_data.find_all('li')
    list_with_data=[]
    for dt in soup_data_final:
        title=dt.text.split('.')[0]
        link=dt.find('a')['href']
        #
        list_with_data.append({
                    "job_title": title,
                    "job_link": link,
                    "company": "CNI",
                    "country": "Romania",
                    "county": 'Bucuresti',
                    "city": 'Bucuresti',
                    "remote": 'on-site'
                })
    return list_with_data
#
print(collect_data_from_API())
#
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


company_name = 'CNI'  # add test comment
data_list = collect_data_from_API()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('CNI',
                  'https://www.cni.ro/cni.jpg'
                  ))