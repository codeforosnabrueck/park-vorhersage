"""
Created on 16.03.2019

@author: wagnerpeer

Module is used to define a database schema to hold general parking ramp
information and details about their capacity using sqlalchemy.
"""
__all__ = ["Capacity", "ParkingRamp", "Session"]

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

_ENGINE = create_engine("sqlite:///opg.db", echo=True)

Session = sessionmaker(bind=_ENGINE)

Base = declarative_base()


class ParkingRamp(Base):
    __tablename__ = "parking_ramps"

    identifier = Column(Integer, primary_key=True)
    name = Column(String)
    street = Column(String)
    zipCode = Column(String)
    city = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    address = Column(String)
    tstamp = Column(Integer)


class Capacity(Base):
    __tablename__ = "capacities"

    identifier = Column(Integer, primary_key=True)
    access_time = Column(Integer)
    free_capacity = Column(Integer)
    total_capacity = Column(Integer)
    parking_ramp_identifier = Column(Integer, ForeignKey("parking_ramps.identifier"))

    parking_ramp = relationship("ParkingRamp", back_populates="capacities")


ParkingRamp.capacities = relationship(
    "Capacity", order_by=Capacity.identifier, back_populates="parking_ramp"
)


def store(data):
    session = Session()

    for ramp in data.values():
        capacity = Capacity(**ramp.pop("utilization"))

        parking_ramp = session.query(ParkingRamp).get(ramp["identifier"])

        if parking_ramp is None:
            parking_ramp = ParkingRamp(**ramp)
            session.add(parking_ramp)

        parking_ramp.capacities.append(capacity)

    session.commit()
