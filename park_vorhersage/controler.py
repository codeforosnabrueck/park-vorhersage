"""
Created on 16.03.2019

@author: wagnerpeer

Module is used to combine scraper and storage system to persist parking ramp
information from the official OPG website https://www.parken-osnabrueck.de/
It can also be used to create the database from the schema definition.
"""
__all__ = ["init", "scrape_and_store"]

from .storage import Base, Session, store
from .scraper import scrape


def init():
    session = Session()
    Base.metadata.create_all(session.bind)


def scrape_and_store():
    data = scrape()
    store(data)
