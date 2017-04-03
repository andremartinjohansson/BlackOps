#!/usr/bin/env python3

""" Missions """

from sqlalchemy import Column, String, Integer
from base import Base
from copy import deepcopy
from random import random

class Missions(Base):
    """ Missions """
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    villain_names = Column(String)
    attributes = Column(String)
    heroes = []
    villains = []
    defeated_heroes = []
    defeated_villains = []

    def __init__(self, name, villain_names, attributes):
        self.name = name
        self.villain_names = villain_names
        self.attributes = attributes

    def the_villains(self, all_villains):
        """ Return mission villains """
        self.villains = self.villain_names.split(" | ")
        self.villains.pop(-1)
        temp = []
        for villain_name in self.villains:
            for villain in all_villains:
                if villain_name == villain.name:
                    temp.append(villain)
        self.villains = temp

    def setup_heroes_table(self, all_heroes):
        """ Do heroes table """
        heroes_table = ""
        for hero in all_heroes:
            heroes_table += """<tr><td><input type='checkbox' name='{name}' value='{id}'</td>
            <td><img class="avatar" src="static/images/{avatar}"></td>
            <td>{name}</td>
            <td>{hp}</td>
            <td>{defense}</td>
            <td>{dmg}</td>
            <td>{catch_rate}</td></tr>""".format(id=hero.id, \
            name=hero.name, hp=hero.hp, defense=hero.defense, dmg=hero.dmg, catch_rate=hero.catch_rate, \
            avatar=hero.avatar)
        return heroes_table

    def setup_villains_table(self):
        """ Do villains table """
        setup_villains_table = ""
        for villain in self.villains:
            setup_villains_table += """<tr><td><img class="avatar" src="static/images/{avatar}"></td>
            <td>{name}</td>
            <td>{hp}</td>
            <td>{defense}</td>
            <td>{dmg}</td>
            <td>{catch_rate}</td></tr>""".format(name=villain.name, \
            hp=villain.hp, defense=villain.defense, dmg=villain.dmg, catch_rate=villain.catch_rate, \
            avatar=villain.avatar)
        return setup_villains_table

    def mission_attributes(self):
        """ Attributes effects """
        copy_heroes = deepcopy(self.heroes)
        copy_villains = deepcopy(self.villains)
        mission_attributes = self.attributes.split(" | ")
        mission_attributes.pop(-1)
        for hero in copy_heroes:
            if "Kryptonite" in mission_attributes and hero.name == "Superman":
                hero.defense = hero.defense / 2
            if "Broken Armor" in mission_attributes and hero.name == "Batman":
                hero.defense = hero.defense * 0.8
            if "Slow Serum" in mission_attributes and hero.name == "The Flash":
                hero.catch_rate = hero.catch_rate / 2
                hero.defense = hero.defense * 0.75
        for villain in copy_villains:
            if "Radiation" in mission_attributes and villain.name == "Godzilla":
                villain.hp = villain.hp * 1.25
            if "Heat" in mission_attributes and villain.name == "Killer Frost":
                villain.hp = villain.hp * 0.8
            if "Power Limitation" in mission_attributes and villain.name == "Zoom":
                villain.catch_rate = villain.catch_rate / 4
        self.heroes = copy_heroes
        self.villains = copy_villains

    def fight(self):
        """ Fight """
        for hero in self.heroes:
            # print("NEW HERO")
            for villain in self.villains:
                # print("NEW VILLAIN")
                if hero in self.defeated_heroes:
                    continue
                if villain in self.defeated_villains:
                    continue
                while villain.hp > 0 and hero.hp > 0:
                    print(hero.name + " vs " + villain.name)
                    villain.hp = villain.hp - (hero.dmg * ((villain.defense / 100)))
                    if villain.hp <= 0:
                        print(villain.name + " was deafeated.")
                        villain.hp = 0
                        self.defeated_villains.append(villain)
                        break
                    hero.hp = hero.hp - (villain.dmg * ((hero.defense / 100)))
                    if hero.hp <= 0:
                        print(hero.name + " was deafeated.")
                        hero.hp = 0
                        self.defeated_heroes.append(hero)
                        break
                    if random() < hero.catch_rate:
                        print(villain.name + " was captured.")
                        self.defeated_villains.append(villain)
                        break
                    if random() < villain.catch_rate:
                        print(hero.name + " was captured.")
                        self.defeated_heroes.append(hero)
                        break
        return [self.heroes, self.villains]

    def won(self):
        """ Did heroes win? """
        if len(self.defeated_heroes) == len(self.heroes):
            won = False
        elif len(self.defeated_villains) == len(self.villains):
            won = True
        return won
