##
#
#
# New scraper for -> Apanova Bucuresti
# Acronis job page -> https://www.apanovabucuresti.ro/despre-noi/cariere
from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
#
import requests
from bs4 import BeautifulSoup
import uuid
#
def collect_data_from_API():
# function to return a list with JSON data
    response=requests.get ('https://www.apanovabucuresti.ro/despre-noi/cariere', headers=DEFAULT_HEADERS)
    soup=BeautifulSoup(response.text, 'lxml')
    soup_data =soup.find_all('div', class_="jobInfo")
    list_with_data=[]
    for dt in soup_data:
        title=dt.find('a').text
        link=dt.find('a')['href']
        #
        list_with_data.append({
                    "id": str(uuid.uuid4()),
                    "job_title": title,
                    "job_link":  'https://www.apanovabucuresti.ro/despre-noi/' + link,
                    "company": "Apanova",
                    "country": "Romania",
                    "city": 'Bucuresti'
                })
    return list_with_data
#
print(collect_data_from_API())
