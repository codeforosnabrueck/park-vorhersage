"""
Created on 16.01.2019

@author: wagnerpeer

Module is used to extract general information about parking ramps and details
about their capacity from the official OPG website:
https://www.parken-osnabrueck.de/
"""
import datetime
import html
import json
import logging
import re
from urllib import error, request, robotparser

import pytz

AGENT_NAME = "codeforosnabrueckbot"

TIMEZONE_OSNABRUECK = pytz.timezone("Europe/Berlin")

logger = logging.getLogger("opg_scraper." + __name__)


def raise_for_status(response):
    """Raises stored :class:`HTTPError`, if one occurred.
    
    Taken from requests library.
    See: https://2.python-requests.org/en/master/_modules/requests/models/#Response.raise_for_status
    """

    http_error_msg = ""
    if isinstance(response.reason, bytes):
        # We attempt to decode utf-8 first because some servers
        # choose to localize their reason strings. If the string
        # isn't utf-8, we fall back to iso-8859-1 for all other
        # encodings. (See PR #3538)
        try:
            reason = response.reason.decode("utf-8")
        except UnicodeDecodeError:
            reason = response.reason.decode("iso-8859-1")
    else:
        reason = response.reason

    if 400 <= response.status < 500:
        http_error_msg = u"%s Client Error: %s for url: %s" % (
            response.status,
            reason,
            response.url,
        )

    elif 500 <= response.status < 600:
        http_error_msg = u"%s Server Error: %s for url: %s" % (
            response.status,
            reason,
            response.url,
        )

    if http_error_msg:
        raise error.HTTPError(
            url=response.geturl(),
            code=response.getcode(),
            msg=http_error_msg,
            hdrs=response.info(),
            fp=None,
        )


def raise_for_robots_txt(url, agent_name=AGENT_NAME):
    parser = robotparser.RobotFileParser(url)
    parser.read()

    if not parser.can_fetch(agent_name, url):
        raise PermissionError(
            "The robots.txt permitts the crawling of the site {}".format(url)
        )


def get_details(url=None):
    with request.urlopen(url) as response:
        raise_for_status(response)
        page_source = response.read().decode()

    utilization = json.loads(page_source)

    utilization["access_time"] = datetime.datetime.now(tz=TIMEZONE_OSNABRUECK)

    return utilization


def get_general_info():
    url = r"https://www.parken-osnabrueck.de/"

    raise_for_robots_txt(url)

    with request.urlopen(url) as response:
        raise_for_status(response)
        page_source = response.read().decode()

    parking_ramps = re.search(
        pattern=r"var parkingRampData = (\{.*\});", string=page_source
    )

    parking_ramps = json.loads(html.unescape(parking_ramps.group(1)))

    utilization = get_details(
        r"https://www.parken-osnabrueck.de/index.php?type=427590&tx_tiopgparkhaeuserosnabrueck_parkingosnabruek[controller]=Parking&tx_tiopgparkhaeuserosnabrueck_parkingosnabruek[action]=ajaxCallGetUtilizationData&_=1556046149040"
    )

    for identifier, ramp_data in parking_ramps.items():
        logger.info("Parking Ramp Name: %s", ramp_data["name"])

        details = utilization["ramp-" + identifier]

        logger.info(("{available} von {capacity} frei.").format(**details))

        ramp_data["utilization"] = {
            "free_capacity": details["available"],
            "total_capacity": details["capacity"],
            "access_time": utilization["access_time"],
        }

        del ramp_data["gmapsMarker"]

    return parking_ramps


def scrape():
    return get_general_info()
