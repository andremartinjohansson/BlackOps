#!/usr/bin/env python3

""" Results """

from sqlalchemy import Column, String, Integer, Boolean
from base import Base

class Results(Base):
    """ Results """
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    mission = Column(String)
    won = Column(Boolean)
    heroes = Column(String)
    villains = Column(String)
    attributes = Column(String)

    def __init__(self, mission, won, stats, attributes):
        self.mission = mission
        self.won = won
        self.heroes = stats[0]
        self.villains = stats[1]
        self.attributes = attributes

    def the_heroes(self):
        """ Result heroes """
        result_heroes_table = ""
        mission_heroes = self.heroes.split(" | ")
        mission_heroes.pop(-1)
        for mission_hero in mission_heroes:
            stats = mission_hero.split(", ")
            result_heroes_table += """<tr><td><img class="avatar" src="static/images/{avatar}"></td>
            <td>{name}</td>
            <td>{hp}</td>
            <td>{defense}</td>
            <td>{dmg}</td>
            <td>{catch_rate}</td></tr>""".format(name=stats[0], \
            hp=stats[1], defense=stats[2], dmg=stats[3], catch_rate=stats[4], \
            avatar=stats[5])
        return result_heroes_table

    def the_villains(self):
        """ Result villains """
        result_villains_table = ""
        mission_villains = self.villains.split(" | ")
        mission_villains.pop(-1)
        for mission_villain in mission_villains:
            stats = mission_villain.split(", ")
            result_villains_table += """<tr><td><img class="avatar" src="static/images/{avatar}"></td>
            <td>{name}</td>
            <td>{hp}</td>
            <td>{defense}</td>
            <td>{dmg}</td>
            <td>{catch_rate}</td></tr>""".format(name=stats[0], \
            hp=stats[1], defense=stats[2], dmg=stats[3], catch_rate=stats[4], \
            avatar=stats[5])
        return result_villains_table
