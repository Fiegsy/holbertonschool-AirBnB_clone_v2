#!/usr/bin/python3
"""State Module for HBNB project."""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class State(BaseModel, Base):
    """State class for the HBNB project."""
    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship("City", back_populates="state", cascade="all, delete")

    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Getter attribute.
            Returns the list of City instances with state_id matching
            the current State.id"""
            from models import storage

            my_cities = []
            for city in storage.all(City).values():
                if self.id == city.state_id:
                    my_cities.append(city)
            return my_cities
