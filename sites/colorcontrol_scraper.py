# New scraper for -> Color Control
# Job page -> https://colorcontrol.ro/vacancies

import re

import requests

from A_OO_get_post_soup_update_dec import DEFAULT_HEADERS, update_peviitor_api
from L_00_logo import update_logo


VACANCIES_URL = 'https://colorcontrol.ro/vacancies'
BUNDLE_URL = 'https://colorcontrol.ro/assets/index-BHDMwuLD.js'
COMPANY_CITY = 'Apahida'
COMPANY_COUNTY = 'Cluj'


def collect_data_from_API():
    """Return current vacancies from the site bundle."""

    response = requests.get(BUNDLE_URL, headers=DEFAULT_HEADERS)
    vacancy_pattern = re.compile(
        r'id:"([^"]+)",title:"([^"]+)"(?:,titleRo:"([^"]+)")?,'
        r'department:"([^"]+)"(?:,departmentRo:"([^"]+)")?,'
        r'location:"([^"]+)"(?:,locationRo:"([^"]+)")?,type:"([^"]+)"'
    )

    list_with_data = []
    for job_id, title, title_ro, _department, _department_ro, location, _location_ro, job_type in vacancy_pattern.findall(response.text):
        city = COMPANY_CITY
        county = COMPANY_COUNTY

        if 'Apahida' in location:
            city = 'Apahida'
        elif 'Cluj-Napoca' in location:
            city = 'Cluj-Napoca'
        elif 'Sannicoara' in location or 'Sânnicoara' in location:
            city = 'Sannicoara'

        list_with_data.append({
            "job_title": title_ro or title,
            "job_link": f'{VACANCIES_URL}#{job_id}',
            "company": "Colorcontrol",
            "country": "Romania",
            "county": county,
            "city": city,
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


company_name = 'Colorcontrol'
data_list = collect_data_from_API()
scrape_and_update_peviitor(company_name, data_list)

update_logo('Colorcontrol',
            'https://www.colorcontrol.ro/og-image.png'
            )
