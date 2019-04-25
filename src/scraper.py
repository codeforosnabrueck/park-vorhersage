"""
Created on 16.01.2019

@author: wagnerpeer

Module is used to extract general information about parking ramps and details
about their capacity from the official OPG website:
https://www.parken-osnabrueck.de/
"""
import html
import json
import logging
import re
import time
from urllib import robotparser

from bs4 import BeautifulSoup

import requests


AGENT_NAME = 'codeforosnabrueckbot'


logger = logging.getLogger('opg_scraper.' + __name__)


def raise_for_robots_txt(url, agent_name=AGENT_NAME):
    parser = robotparser.RobotFileParser(url)
    parser.read()

    if not parser.can_fetch(agent_name, url):
        raise PermissionError(f'The robots.txt permitts the crawling of the '
                              'site {url}')


def get_details(url=None):
    response = requests.get(url)
    response.raise_for_status()
    utilization = json.loads(response.content.decode(response.encoding))

    return utilization


def get_general_info():
    url = r'https://www.parken-osnabrueck.de/'

    raise_for_robots_txt(url)

    response = requests.get(url)
    response.raise_for_status()
    page_source = response.content.decode(response.encoding)

    parking_ramps = re.search(pattern='var parkingRampData = (\{.*\});',
                              string=page_source)

    parking_ramps = json.loads(html.unescape(parking_ramps.group(1)))

    utilization = get_details(r'https://www.parken-osnabrueck.de/index.php?type=427590&tx_tiopgparkhaeuserosnabrueck_parkingosnabruek[controller]=Parking&tx_tiopgparkhaeuserosnabrueck_parkingosnabruek[action]=ajaxCallGetUtilizationData&_=1556046149040')

    for identifier, ramp_data in parking_ramps.items():
        logger.info(f'Parking Ramp Name: {ramp_data["name"]}')

        details = utilization['ramp-' + identifier]

        logger.info((f'{details["available"]} von {details["capacity"]} frei.'))

        ramp_data['free_capacity'] = details['available']
        ramp_data['total_capacity'] = details['capacity']

        del ramp_data['gmapsMarker']

    return parking_ramps


def scrape():
    return get_general_info()
