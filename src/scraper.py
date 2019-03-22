"""
Created on 16.01.2019

@author: wagnerpeer

Module is used to extract general information about parking ramps and details
about their capacity from the official OPG website:
https://www.parken-osnabrueck.de/
"""
from contextlib import contextmanager
import functools
import html
import json
import logging
import re
import time
from urllib import robotparser

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException


AGENT_NAME = 'codeforosnabrueckbot'


logger = logging.getLogger('opg_scraper.' + __name__)


def eval_robots_txt(agent_name):
    @functools.wraps
    def inner(func):
        def wrapper(*args, **kwargs):
            parser = robotparser.RobotFileParser(url=kwargs['url'])
            parser.read()

            if parser.can_fetch(agent_name, kwargs['url']):
                return func(*args, **kwargs)
            else:
                raise PermissionError(f'The robots.txt permitts the crawling of the site {kwargs["url"]}')
        return wrapper
    return inner


def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 2)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except TimeoutException:
        logger.info('Timeout reached while waiting for website to load!')


@eval_robots_txt(AGENT_NAME)
def get_details(driver, *, url=None):
    # Get handle to send shortcut which opens new tab
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    driver.get(url)
    wait_for_ajax(driver)

    total_capacity = driver.find_element_by_class_name('detail-total-capacity').text
    free_capacity = driver.find_element_by_class_name('detail-free-capacity').text

    logger.info((f'{free_capacity} von {total_capacity} frei.'))

    # Get handle to send shortcut which closes current tab
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

    return int(free_capacity), int(total_capacity)


@eval_robots_txt(AGENT_NAME)
def get_general_info(driver, *, url=None):
    driver.get(url)
    wait_for_ajax(driver)
    # wait_for_ajax` function might not work as expected, add extra sleep
    time.sleep(1)

    page_source = driver.page_source

    parking_ramps = re.search(pattern='var parkingRampData = (\{.*\});',
                              string=page_source)

    parking_ramps = json.loads(html.unescape(parking_ramps.group(1)))

    for identifier, ramp_data in parking_ramps.items():
        logger.info(f'Parking Ramp Name: {ramp_data["name"]}')

        soup = BeautifulSoup(ramp_data['gmapsMarker'], 'html.parser')
        details_url = soup.find('a', 'opg-map-infowindow-detaillink').get('href').replace('\\', '')

        free_capacity, total_capacity = get_details(driver=driver, url=details_url)
        ramp_data['free_capacity'] = free_capacity
        ramp_data['total_capacity'] = total_capacity

        del ramp_data['gmapsMarker']

    return parking_ramps


def scrape(url):
    with get_webdriver() as driver:
        return get_general_info(driver=driver, url=url)


@contextmanager
def get_webdriver():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.close()
    driver.quit()
