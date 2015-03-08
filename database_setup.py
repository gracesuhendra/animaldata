import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class Animal(Base):
    __tablename__ = 'animal'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name'  : self.name,
            'id'    : self.id,
        }

class PetItem(Base):
    __tablename__ = 'pet_item'

    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    gender = Column(String(250))
    animal_id = Column(Integer, ForeignKey('animal.id'))
    animal = relationship(Animal)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'gender': self.gender,
            }

engine = create_engine('sqlite:///animalpet.db')
Base.metadata.create_all(engine)
    
            
