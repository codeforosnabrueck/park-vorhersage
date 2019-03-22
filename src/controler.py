"""
Created on 16.03.2019

@author: wagnerpeer

Module is used to combine scraper and storage system to persist parking ramp
information from the official OPG website https://www.parken-osnabrueck.de/
It can also be used to create the database from the schema definition.
"""
from . import Session

from .storage import Base, ParkingRamp, Capacity
from .scraper import scrape


def create():
    session = Session()
    Base.metadata.create_all(session.bind)


def scrape_website():
    url = r'https://www.parken-osnabrueck.de/'
    return scrape(url)


def _create_or_retrieve_objects(tstamp=None,
                                free_capacity=None,
                                total_capacity=None,
                                **kwargs):
    session = Session()

    parking_ramp = session.query(ParkingRamp).get(kwargs['identifier'])

    if parking_ramp is None:
        parking_ramp = ParkingRamp(**kwargs)

    capacity = Capacity(tstamp=tstamp,
                        free_capacity=free_capacity,
                        total_capacity=total_capacity)
    return parking_ramp, capacity


def store_data(data):
    session = Session()

    for ramp in data.values():
        capacity = Capacity(tstamp=ramp.pop('tstamp'),
                            free_capacity=ramp.pop('free_capacity'),
                            total_capacity=ramp.pop('total_capacity'))

        parking_ramp = session.query(ParkingRamp).get(ramp['identifier'])

        if parking_ramp is None:
            parking_ramp = ParkingRamp(**ramp)
            session.add(parking_ramp)

        parking_ramp.capacities.append(capacity)

    session.commit()


def scrape_and_store():
    data = scrape_website()
    store_data(data)
