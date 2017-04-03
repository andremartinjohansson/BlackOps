#!/usr/bin/env python3

""" Test characters """

import unittest
from characters import Heroes, Villains

class TestChars(unittest.TestCase):
    """ Test character classes """

    the_flash = Heroes(["The Flash", 150, 50, 100, 75, "Flash-Lightning-Icon.png"])
    zoom = Villains(["Zoom", 200, 70, 130, 40, "Zoom-Super-Speed.png"])

    def test_zoom_name(self):
        """ Get Zoom's name """
        self.assertEqual(self.zoom.name, "Zoom")

    def test_flash_hp(self):
        """ Get HP of The Flash """
        self.assertEqual(self.the_flash.hp, 150)

    def test_zoom_dmg(self):
        """ Get DMG of Zoom """
        self.assertEqual(self.zoom.dmg, 130)

    def test_flash_defense(self):
        """ Get Defense of The Flash """
        self.assertEqual(self.the_flash.defense, 50)

    def test_fight_damage(self):
        """ Test fight damage """
        damaged = self.the_flash.hp - (self.zoom.dmg * ((self.the_flash.defense / 100) / 10))
        self.assertNotEqual(damaged, 150)

    def test_catch_rates(self):
        """ Test catch rates """
        self.assertTrue(self.the_flash.catch_rate > self.zoom.catch_rate)

    def test_fight_winner(self):
        """ Test who wins the fight, without catch rates """
        flash_health = self.the_flash.hp
        zoom_health = self.zoom.hp
        while True:
            flash_health = flash_health - (self.zoom.dmg * ((self.the_flash.defense / 100) / 10))
            zoom_health = zoom_health - (self.the_flash.dmg * ((self.zoom.defense / 100) / 10))
            if flash_health <= 0:
                won = False
                break
            elif zoom_health <= 0:
                won = True
                break
        self.assertFalse(won)

    def test_flash_avatar(self):
        """ Test avatar """
        url = "static/images/" + self.the_flash.avatar
        self.assertEqual(url, "static/images/Flash-Lightning-Icon.png")

if __name__ == '__main__':
    unittest.main()
