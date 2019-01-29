from contextlib import contextmanager
import functools
import time
from urllib import robotparser

from bs4 import BeautifulSoup
# import cachetools
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

AGENT_NAME = 'codeforosnabrueckbot'


def eval_robots_txt(agent_name, url):
    def inner(func):
        @functools.wraps
        def wrapper(*args, **kwargs):
            parser = robotparser.RobotFileParser(url=kwargs['url'])
            parser.read()

            if parser.can_fetch(agent_name, kwargs['url']):
                return func(*args, **kwargs)
            else:
                raise PermissionError(f'The robots.txt permitts the crawling of the site {url}')
        return wrapper
    return inner


def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 5)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass


def get_details(driver, url):
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    driver.get(url)
    wait_for_ajax(driver)

    total_capacity = driver.find_element_by_class_name('detail-total-capacity').text
    free_capacity = driver.find_element_by_class_name('detail-free-capacity').text

    longitude = driver.find_element_by_xpath('//meta[@property=\'og:longitude\']').get_attribute('content')
    latitude = driver.find_element_by_xpath('//meta[@property=\'og:latitude\']').get_attribute('content')

    print(f'{free_capacity} von {total_capacity} frei.')
    print(f'Parkplatz Geolocation: {latitude}lat, {longitude}lng')

    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')


def get_general_info(*, url=None):
    pass


def main(driver, url):

    driver.get(url)
    wait_for_ajax(driver)
    time.sleep(3)

    parking_ramp_list = driver.find_element_by_class_name('parking-ramp-list')
    ramp_ids = [parking_ramp.get_attribute('class') for parking_ramp in parking_ramp_list.find_elements_by_class_name('parking-ramp-item')]

    for parking_ramp_class in ramp_ids:
        parking_ramp = driver.find_element_by_class_name(parking_ramp_class.strip('.'))
        link_tag = parking_ramp.find_element_by_tag_name('a')
        details_url = link_tag.get_attribute('href')
        try:
            parking_ramp_name = link_tag.find_element_by_class_name('parking-ramp-name').text
            parking_ramp_utilization = link_tag.find_element_by_class_name('parking-ramp-utilization').text
            if parking_ramp_name and parking_ramp_utilization:
                print(f'{parking_ramp_name} hat {parking_ramp_utilization}e Plaetze.')# (Fuer mehr Details {details_url})')
                get_details(driver, details_url)
        except NoSuchElementException:
            pass

@contextmanager
def get_webdriver():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


if __name__ == '__main__':
    url = r'https://www.parken-osnabrueck.de/'

    with get_webdriver() as driver:
        # main = eval_robots_txt(url, AGENT_NAME)(main)
        main(driver, url)
