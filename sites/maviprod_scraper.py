##
#
#
# New scraper for -> SC MAVIPROD SRL
# Acronis job page -> https://www.maviprod.ro/despre-noi/cariere/
import requests
import unicodedata
from bs4 import BeautifulSoup

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from __utils import get_county


#
def collect_data_from_API():
# function to return a list with JSON data
    response=requests.get ('https://www.maviprod.ro/despre-noi/cariere/', headers=DEFAULT_HEADERS)
    soup=BeautifulSoup(response.text, 'lxml')
    soup_data =soup.find_all('div', class_='col-sm-4 col-lg-4 col-xs-12 chenar')
    list_with_data=[]
    for dt in soup_data:
        title=dt.find('a').text
        link=dt.find('a')['href']
        city = dt.find('p').text.split(': ')[-1]
        city = unicodedata.normalize('NFKD', city).encode('ascii', 'ignore').decode('utf-8')
        all_towns = city.split(", ")
        all_counties=[]
        for town in all_towns:
            county=get_county(town)
            all_counties.append(county)
        list_with_data.append({
                    "job_title": title,
                    "job_link": link,
                    "company": "maviprod",
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


company_name = 'maviprod' 
data_list = collect_data_from_API()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('maviprod',
                  'https://www.maviprod.ro/wp-content/themes/maviprod/images/logo.png'
                  ))
