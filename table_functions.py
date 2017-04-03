#!/usr/bin/env python3

""" Table Functions """

from characters import Heroes, Villains
from missions import Missions
from results import Results

def do_heroes_table(self):
    """ Create heroes table """
    heroes_table = ""
    all_heroes = self.session.query(Heroes).all()
    for hero in all_heroes:
        heroes_table += """<tr><td><img class="avatar" src="static/images/{avatar}"></td>
        <td>{name}</td>
        <td>{hp}</td>
        <td>{defense}</td>
        <td>{dmg}</td>
        <td>{catch_rate}</td>
        <td><a href='character?edit={name}'>Edit</a></td>
        <td><a href='?del={id}'>Remove</a></td></tr>""".format(id=hero.id, \
        name=hero.name, hp=hero.hp, defense=hero.defense, dmg=hero.dmg, catch_rate=hero.catch_rate, \
        avatar=hero.avatar)
    return heroes_table

def do_villains_table(self):
    """ Create villains table """
    villains_table = ""
    all_villains = self.session.query(Villains).all()
    for villain in all_villains:
        villains_table += """<tr><td><img class="avatar" src="static/images/{avatar}"></td>
        <td>{name}</td>
        <td>{hp}</td>
        <td>{defense}</td>
        <td>{dmg}</td>
        <td>{catch_rate}</td>
        <td><a href='character?edit={name}'>Edit</a></td>
        <td><a href='?del={id}'>Remove</a></td></tr>""".format(id=villain.id, \
        name=villain.name, hp=villain.hp, defense=villain.defense, dmg=villain.dmg, catch_rate=villain.catch_rate, \
        avatar=villain.avatar)
    return villains_table

def do_missions_table(self):
    """ Create missions table """
    missions_table = ""
    all_missions = self.session.query(Missions).all()
    all_villains = self.session.query(Villains).all()
    for mission in all_missions:
        missions_table += """<tr><td><a href='setup_mission?name={name}'>{name}</a></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td><a href='?del={id}'>Remove</a></td></tr>""".format(id=mission.id, name=mission.name)
        mission_villains = mission.villain_names.split(" | ")
        mission_villains.pop(-1)
        for mission_villain in mission_villains:
            for villain in all_villains:
                if mission_villain == villain.name:
                    missions_table += """<tr><td><img class="avatar" src="static/images/{avatar}"></td>
                    <td>{name}</td>
                    <td>{hp}</td>
                    <td>{defense}</td>
                    <td>{dmg}</td>
                    <td>{catch_rate}</td></tr>""".format(name=villain.name, \
                    hp=villain.hp, defense=villain.defense, dmg=villain.dmg, catch_rate=villain.catch_rate, \
                    avatar=villain.avatar)
    return missions_table

def history(self):
    """ Show all previous fights """
    history_table = ""
    all_results = self.session.query(Results).all()
    for result in all_results:
        if result.won == 1:
            res = "Heroes won"
        else:
            res = "Heroes lost"
        history_table += """<tr><td><a href='results?mission={mission}'>{mission}</a></td>
        <td>{result}</td></tr>""".format(mission=result.mission, result=res)
    return history_table
