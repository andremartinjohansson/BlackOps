#!/usr/bin/env python3

""" Test mission """

import unittest
from missions import Missions
from characters import Heroes, Villains

class TestMission(unittest.TestCase):
    """ Test missions class """

    mission = Missions(name="Out of Time", villain_names="The Flash | Zoom | ", \
    attributes="Slow Serum | Power Limitation | ")

    the_flash = Heroes(["The Flash", 150, 50, 100, 75, "Flash-Lightning-Icon.png"])
    zoom = Villains(["Zoom", 200, 70, 130, 40, "Zoom-Super-Speed.png"])

    def test_mission_name(self):
        """ Test the mission name """
        self.assertEqual(self.mission.name, "Out of Time")

    def test_villains(self):
        """ Test villains on mission """
        villains = self.mission.villain_names.split(" | ")
        villains.pop(-1)
        self.assertEqual(villains[0], "The Flash")
        self.assertEqual(villains[1], "Zoom")

    def test_attributes(self):
        """ Test attributes """
        mission_attributes = self.mission.attributes.split(" | ")
        mission_attributes.pop(-1)
        mission_attributes = ", ".join(mission_attributes)
        self.assertEqual(mission_attributes, "Slow Serum, Power Limitation")

    def test_characters(self):
        """ Test mission villains """
        self.mission.the_villains([self.zoom])
        self.mission.heroes.append(self.the_flash)
        self.assertEqual(self.mission.villains[0].name, "Zoom")
        self.assertEqual(self.mission.heroes[0].name, "The Flash")

    def test_attribute_effects(self):
        """ Test effects """
        self.mission.the_villains([self.zoom])
        self.mission.heroes.append(self.the_flash)
        self.mission.mission_attributes()
        self.assertEqual(self.mission.villains[0].catch_rate, 40/4)
        self.assertEqual(self.mission.heroes[0].catch_rate, 75/2)

if __name__ == '__main__':
    unittest.main()
