#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='park-vorhersage',
      version='0.0.1',
      description='Dies ist ein Repository, um die Parkhaus-/Parkplatzdaten der Osnabücker Parkstätten Betriebsgesellschaft (OPG) zu analysieren.',
      author_email='',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3'],
      keywords='parking scraper',
      packages=find_packages(exclude=['test']),
      install_requires=['requests', 'BeautifulSoup4', 'pytz', 'sqlalchemy'],
      python_requires='>=3.5',
      entry_points={
        'console_scripts': [
        'parkvorhersage=park_vorhersage.controler:scrape_and_store',
            ],
        },
)
