from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo
from __utils.found_county import get_county
from bs4 import BeautifulSoup
import requests
import unicodedata
def collect_data_from_API():
    response = requests.get('https://cona.ro/cariere/', headers=DEFAULT_HEADERS)
    soup = BeautifulSoup(response.text, 'lxml')
    #print (soup)
    soup_data = soup.find_all('div', class_="accordion-item")
    #print (soup_data)
    list_with_data = []
    for dt in soup_data:
        title = dt.find('h3').text
        locations=dt.find_all('span', class_="tag_name")
        all_locations=[]
        for loc in locations:
            location_text = loc.text.strip()  # Remove any leading/trailing spaces
            if (location_text == 'Şantiere în ţară') or (location_text =='Sediu Central') or (location_text == 'jud.Sibiu'):
                continue
            else:
                location_text = ''.join(c for c in unicodedata.normalize('NFKD', location_text) if not unicodedata.combining(c))
                all_locations.append(location_text)
        county_list=[]
        for town in all_locations:
            county=get_county(town)
            if county is not None:  # Check for existing town
                county_list.append(county)
        #link = dt.find('a')['href']
        #
        list_with_data.append({
            "job_title": title,
            "job_link": 'https://cona.ro/cariere/'+'#'+title,
            "company": "Cona",
            "country": "Romania",
            "county": county_list,
            "city": all_locations
        })
    return list_with_data
# update data on peviitor!
@update_peviitor_api
def scrape_and_update_peviitor(company_name, data_list):
    return data_list
company_name = 'Cona'
data_list = collect_data_from_API()
print(data_list)
scrape_and_update_peviitor(company_name, data_list)
print(update_logo('Cona', 'https://cona.ro/wp-content/uploads/2023/09/cona-logo-1.svg'))