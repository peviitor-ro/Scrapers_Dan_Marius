# New scraper for -> Color Control
# Job page -> https://www.colorcontrol.ro/cariere/
#
import requests
from bs4 import BeautifulSoup

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo


#
def collect_data_from_API():
# function to return a list with JSON data
    response=requests.get ('https://www.colorcontrol.ro/cariere/', headers=DEFAULT_HEADERS)
    soup=BeautifulSoup(response.text, 'lxml')
    soup_data =soup.find('div', class_="menu-available-jobs-container")
    list_items=soup_data.find_all('li')
    list_with_data=[]
    for dt in list_items:
        title=dt.find('a').text
        link=dt.find('a')['href']
        #
        list_with_data.append({
                    "job_title": title,
                    "job_link": link,
                    "company": "Colorcontrol",
                    "country": "Romania",
                    "county": 'Cluj',
                    "city": 'Cluj-Napoca'
                })
    return list_with_data
#
#
# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    """
    Update data on peviitor API!
    """

    return data_list


company_name = 'Colorcontrol'  # add test comment
data_list = collect_data_from_API()
print(data_list)
scrape_and_update_peviitor(company_name, data_list)

update_logo('Colorcontrol',
                  'https://www.colorcontrol.ro/wp-content/uploads/2016/10/ccs-logo.svg'
                  )