from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
import re
import requests
from bs4 import BeautifulSoup
from __utils import get_county

#
def collect_data_from_API():
# function to return a list with JSON data
    response=requests.get ('https://www.dpd.com/ro/ro/compania-dpd/cariere-profesionale-dpd-ro/', headers=DEFAULT_HEADERS)
    soup=BeautifulSoup(response.text, 'lxml')
    soup_data =soup.find('div', id="pgc-449-2-0")
    soup_data_final= soup_data.find_all('li')
    list_with_data=[]
    city_exists = False
    for dt in soup_data_final:
        title=dt.find('p').text.rstrip()
        words = re.findall(r"\w+", title)
        city=[]
        county=[]
        for word in words:
            if get_county(word) or word=='Cluj':
                if word=='Cluj':
                    word='Cluj-Napoca'
                city_exists=True
                city.append (word)
                county.append (get_county(word))
            else:
                city_exists=False
        if city_exists==True:
            list_with_data.append({
                        "job_title": title,
                        "job_link": 'https://www.dpd.com/ro/ro/compania-dpd/cariere-profesionale-dpd-ro/'+'#'+title,
                        "company": "DPD",
                        "country": "Romania",
                        "county": county,
                        "city": city,
                        "remote": 'on-site'
                    })
        else:
            list_with_data.append({
                        "job_title": title,
                        "job_link": 'https://www.dpd.com/ro/ro/compania-dpd/cariere-profesionale-dpd-ro/'+'#'+title,
                        "company": "DPD",
                        "country": "Romania",
                        "county": 'all',
                        "city": 'all',
                        "remote": 'on-site'
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


company_name = 'DPD'  # add test comment
data_list = collect_data_from_API()
scrape_and_update_peviitor(company_name, data_list)

print(update_logo('DPD',
                  'https://www.dpd.com/wp-content/themes/DPD_NoLogin/images/DPD_logo_redgrad_rgb_responsive.svg'
                  ))