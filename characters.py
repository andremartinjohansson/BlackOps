#!/usr/bin/env python3

""" Characters """

from sqlalchemy import Column, Float, String, Integer
from base import Base

class Heroes(Base):
    """ Heroes """
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hp = Column(Float)
    defense = Column(Integer)
    dmg = Column(Integer)
    catch_rate = Column(Integer)
    avatar = Column(String)

    def __init__(self, args):
        self.name = args[0]
        self.hp = args[1]
        self.defense = args[2]
        self.dmg = args[3]
        self.catch_rate = args[4]
        self.avatar = args[5]

class Villains(Base):
    """ Villains """
    __tablename__ = "villains"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hp = Column(Float)
    defense = Column(Integer)
    dmg = Column(Integer)
    catch_rate = Column(Integer)
    avatar = Column(String)

    def __init__(self, args):
        self.name = args[0]
        self.hp = args[1]
        self.defense = args[2]
        self.dmg = args[3]
        self.catch_rate = args[4]
        self.avatar = args[5]
