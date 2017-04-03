#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Data Module """

class Data():
    """ Data Class """

    def __init__(self):
        self.page_title = "Home"

    def title(self, url):
        """ Generate page title and return it """
        if url == "/":
            self.page_title = "Start"
        elif url == "/heroes":
            self.page_title = "Heroes"
        elif url == "/villains":
            self.page_title = "Villains"
        elif url == "/missions":
            self.page_title = "Missions"
        elif url == "/results":
            self.page_title = "Results"
        elif url == "/setup_mission":
            self.page_title = "Plan"
        elif url == "/history":
            self.page_title = "History"
        elif url == "/character":
            self.page_title = "Training"
        elif url == "/attributes":
            self.page_title = "Attributes"
        else:
            self.page_title = "Error"
        return self.page_title
