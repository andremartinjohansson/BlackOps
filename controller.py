#!/usr/bin/env python3

""" Controller module """

from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from data import Data
from characters import Heroes, Villains
from missions import Missions
from results import Results
from random import randint, shuffle
import table_functions as func

class Controller():
    """ Controller Class """

    def __init__(self):
        engine = create_engine("sqlite:///db/blackops.sqlite", \
        connect_args={'check_same_thread': False})
        Base.metadata.create_all(engine, checkfirst=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.heroes = self.session.query(Heroes).all()
        self.villains = self.session.query(Villains).all()
        self.all_missions = self.session.query(Missions).all()
        self.mission = None
        self.all_results = self.session.query(Results).all()
        self.result = None
        self.attributes = []

        self.data = Data()

    def do_table(self, which):
        """ Create tables """
        if which == "heroes":
            return func.do_heroes_table(self)
        elif which == "villains":
            return func.do_villains_table(self)
        elif which == "missions":
            return func.do_missions_table(self)
        elif which == "history":
            return func.history(self)


    #CHARACTERS#
    ##################################################################

    def add_hero(self):
        """ Add a hero """
        args = [request.form["name"], request.form["hp"], request.form["defense"], \
        request.form["dmg"], request.form["catch_rate"], request.form["avatar"]]
        if not request.form["avatar"]:
            args[5] = "Hero.PNG"

        new_hero = Heroes(args)

        self.heroes.append(new_hero)
        self.session.add(new_hero)
        self.session.commit()

    def add_villain(self):
        """ Add a villain """
        args = [request.form["name"], request.form["hp"], request.form["defense"], \
        request.form["dmg"], request.form["catch_rate"], request.form["avatar"]]
        if not request.form["avatar"]:
            args[5] = "Rogue_Icon.png"

        new_villain = Villains(args)

        self.villains.append(new_villain)
        self.session.add(new_villain)
        self.session.commit()

    def remove_hero(self, del_this_hero):
        """ Remove a hero """
        self.session.query(Heroes).filter(Heroes.id == del_this_hero).delete()
        self.session.commit()
        self.heroes = self.session.query(Heroes).all()

    def remove_villain(self, del_this_villain):
        """ Remove a villain """
        self.session.query(Villains).filter(Villains.id == del_this_villain).delete()
        self.session.commit()
        self.villains = self.session.query(Villains).all()

    def get_character(self, character_name):
        """ Get character name """
        for hero in self.heroes:
            if hero.name == character_name:
                attr = ["heroes", hero.name, hero.hp, hero.defense, hero.dmg, hero.catch_rate, \
                hero.avatar, hero.id]
                return attr
        for villain in self.villains:
            if villain.name == character_name:
                attr = ["villains", villain.name, villain.hp, villain.defense, villain.dmg, \
                villain.catch_rate, villain.avatar, villain.id]
                return attr

    def edit_character(self):
        """ Edit character """
        c_type = request.form["type_of_character"]
        if c_type == "heroes":
            for hero in self.heroes:
                if hero.id == int(request.form["id"]):
                    hero.name = request.form["name"]
                    hero.hp = float(request.form["hp"])
                    hero.defense = float(request.form["defense"])
                    hero.dmg = float(request.form["dmg"])
                    hero.catch_rate = float(request.form["catch_rate"])
                    hero.avatar = request.form["avatar"]
        elif c_type == "villains":
            for villain in self.villains:
                if villain.id == int(request.form["id"]):
                    villain.name = request.form["name"]
                    villain.hp = float(request.form["hp"])
                    villain.defense = float(request.form["defense"])
                    villain.dmg = float(request.form["dmg"])
                    villain.catch_rate = float(request.form["catch_rate"])
                    villain.avatar = request.form["avatar"]
        self.session.commit()
        return c_type

    #MISSIONS#
    ##################################################################

    def add_mission(self):
        """ Add a mission """
        effects = ["Kryptonite", "Broken Armor", "Slow Serum", \
        "Radiation", "Heat", "Power Limitation"]
        nr_of_attr = randint(0, len(effects))
        shuffle(effects)
        attributes = ""
        for i in range(0, nr_of_attr):
            attributes += effects[i] + " | "
        nr_of_villains = len(self.villains)
        if nr_of_villains >= 1:
            mission_villains = []
            how_many = randint(1, nr_of_villains)
            for i in range(0, how_many):
                mission_villains.append(self.villains[i].name)
            shuffle(mission_villains)
            villains = ""
            for villain in mission_villains:
                villains += villain + " | "

        new_mission = Missions(name=request.form["name"], villain_names=villains, attributes=attributes)

        self.all_missions.append(new_mission)
        self.session.add(new_mission)
        self.session.commit()

    def remove_mission(self, del_this_mission):
        """ Remove a mission """
        self.session.query(Missions).filter(Missions.id == del_this_mission).delete()
        self.session.commit()
        self.all_missions = self.session.query(Missions).all()

    def set_mission(self, mission_name):
        """ Set active mission """
        for mission in self.all_missions:
            if mission.name == mission_name:
                self.mission = mission
        self.mission.the_villains(self.villains)

    def get_mission_attributes(self):
        """ Get mission attributes """
        mission_attributes = self.mission.attributes.split(" | ")
        mission_attributes.pop(-1)
        self.attributes = mission_attributes
        mission_attributes = ", ".join(mission_attributes)
        return mission_attributes

    def setup_heroes(self):
        """ Create heroes table """
        return self.mission.setup_heroes_table(self.heroes)

    def setup_villains(self):
        """ Show villains you're up against """
        return self.mission.setup_villains_table()

    #FIGHTS#
    ##################################################################

    def chosen_heroes(self):
        """ Save chosen heroes """
        heroes = []
        for value in request.form:
            heroes.append(value)
        for hero in self.heroes:
            for i in range(0, len(heroes)):
                if hero.name == heroes[i]:
                    self.mission.heroes.append(hero)

    def battle(self):
        """ Fight and determine result """
        print("Begin mission {}!".format(self.mission.name))
        self.mission.mission_attributes()
        characters = self.mission.fight()
        won = self.mission.won()
        hero_stats = ""
        villain_stats = ""
        attr = ""
        for hero in characters[0]:
            hero_stats += "{name}, {hp}, {defense}, {dmg}, {catch_rate}, {img} | ".format(\
            name=hero.name, hp=hero.hp, defense=hero.defense, dmg=hero.dmg, \
            catch_rate=hero.catch_rate, img=hero.avatar)
        for villain in characters[1]:
            villain_stats += "{name}, {hp}, {defense}, {dmg}, {catch_rate}, {img} | ".format(\
            name=villain.name, hp=villain.hp, defense=villain.defense, dmg=villain.dmg, \
            catch_rate=villain.catch_rate, img=villain.avatar)
        stats = [hero_stats, villain_stats]
        for a in self.attributes:
            attr += a + " | "
        the_result = Results(mission=self.mission.name, won=won, stats=stats, attributes=attr)

        self.all_results.append(the_result)
        self.session.add(the_result)
        self.remove_mission(self.mission.id)
        return self.mission.name

    #RESULTS#
    ##################################################################

    def get_result(self, mission_name):
        """ Return if won or not """
        for result in self.all_results:
            if result.mission == mission_name:
                self.result = result
                return result.won

    def result_heroes(self, mission_name):
        """ Heroes who were in the fight """
        for result in self.all_results:
            if result.mission == mission_name:
                return result.the_heroes()

    def result_villains(self, mission_name):
        """ Villains who were in the fight """
        for result in self.all_results:
            if result.mission == mission_name:
                return result.the_villains()

    def get_result_attributes(self, mission_name):
        """ Get result attributes """
        for result in self.all_results:
            if result.mission == mission_name:
                result_attributes = result.attributes.split(" | ")
                result_attributes.pop(-1)
                result_attributes = ", ".join(result_attributes)
                return result_attributes
