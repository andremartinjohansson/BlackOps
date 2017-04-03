#!/usr/bin/env python3
"""
My first Flask app
"""
# Importera relevanta moduler
from flask import Flask, render_template, request, flash, redirect
import os
from controller import Controller
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///db/blackops.sqlite")

Session = sessionmaker(bind=engine)
session = Session()

random_key_string = os.urandom(12)

app = Flask(__name__)
app.secret_key = random_key_string

# Make it easier to debug
app.debug = True
app.config.update(
    PROPAGATE_EXCEPTIONS=True
)

func = Controller()

data = func.data

@app.route("/")
def main():
    """ Main route """
    return render_template("index.html", title=data.title("/"))

@app.route("/heroes", methods=["POST", "GET"])
def show_heroes():
    """ Handle GET and POST """
    if request.method == "POST":
        func.add_hero()
        flash('Added hero', 'success')
    if request.method == "GET":
        del_this_hero = request.args.get("del")
        if del_this_hero != None:
            func.remove_hero(del_this_hero)
            flash('Removed hero', 'success')
    return render_template("heroes.html", heroes_table=func.do_table("heroes"), \
    title=data.title("/heroes"))
def heroes():
    """ Heroes route """
    return render_template("heroes.html", title=data.title("/heroes"))

@app.route("/villains", methods=["POST", "GET"])
def show_villains():
    """ Handle GET and POST """
    if request.method == "POST":
        func.add_villain()
        flash('Added villain', 'success')
    if request.method == "GET":
        del_this_villain = request.args.get("del")
        if del_this_villain != None:
            func.remove_villain(del_this_villain)
            flash('Removed villain', 'success')
    return render_template("villains.html", villains_table=func.do_table("villains"), \
    title=data.title("/villains"))
def villains():
    """ Villains route """
    return render_template("villains.html", title=data.title("/villains"))

@app.route("/character", methods=["POST", "GET"])
def edit_character():
    """ Handle GET and POST """
    if request.method == "POST":
        c_type = func.edit_character()
        return redirect(c_type)
    if request.method == "GET":
        character_name = request.args.get("edit")
        if character_name != None:
            atts = func.get_character(character_name)
    return render_template("character.html", title=data.title("/character"), \
    name=atts[1], hp=atts[2], defense=atts[3], dmg=atts[4], catch_rate=atts[5], \
    avatar=atts[6], type=atts[0], id=atts[7])
def character():
    """ Character route """
    return render_template("character.html", title=data.title("/character"))

@app.route("/missions", methods=["POST", "GET"])
def show_missions():
    """ Handle GET and POST """
    if request.method == "POST":
        func.add_mission()
        flash('Added mission', 'success')
    if request.method == "GET":
        del_this_mission = request.args.get("del")
        if del_this_mission != None:
            func.remove_mission(del_this_mission)
            flash('Mission deleted', 'success')
    return render_template("missions.html", missions_table=func.do_table("missions"), \
    title=data.title("/missions"))
def missions():
    """ Mission route """
    return render_template("missions.html", title=data.title("/missions"))

@app.route("/setup_mission", methods=["POST", "GET"])
def show_setup_mission():
    """ Handle GET and POST """
    if request.method == "POST":
        func.chosen_heroes()
        mission_name = func.battle()
        return redirect("results?mission=" + mission_name)
    if request.method == "GET":
        mission_name = request.args.get("name")
        if mission_name != None:
            func.set_mission(mission_name)
            vil_table = func.setup_villains()
            her_table = func.setup_heroes()
            atts = func.get_mission_attributes()
    return render_template("setup_mission.html", villains_table=vil_table, \
    heroes_table=her_table, title=data.title("/setup_mission"), attr=atts)
def setup_mission():
    """ Mission setup route """
    return render_template("setup_mission.html", title=data.title("/setup_mission"))

@app.route("/results", methods=["GET"])
def show_result():
    """ Handle GET """
    if request.method == "GET":
        mission_name = request.args.get("mission")
        if mission_name != None:
            vil_table = func.result_villains(mission_name)
            her_table = func.result_heroes(mission_name)
            res = func.get_result(mission_name)
            atts = func.get_result_attributes(mission_name)
    return render_template("results.html", villains_table=vil_table, heroes_table=her_table, \
    won=res, mission_name=mission_name, title=data.title("/results"), attr=atts)
def results():
    """ Results route """
    return render_template("results.html", title=data.title("/results"))

@app.route("/history")
def history():
    """ Results route """
    return render_template("history.html", title=data.title("/history"), \
    history_table=func.do_table("history"))

@app.route("/attributes")
def attributes():
    """ Attributes route """
    return render_template("attributes.html", title=data.title("/attributes"))


if __name__ == "__main__":
    app.run()
