import pygame
from support import support_folder
from player import Player
class droppable():
    def __init__(self,screen):


        # Getting dimensions of the user screen
        self.screen = screen
        self.MAX_WIDTH = self.screen.get_width()
        self.MAX_HEIGHT = self.screen.get_height()

        self.attributes = {'Duration': 5000, 'Health Boost': 20}

    def import_health_orb_assets(self):
        health_orb_path = "Sprites/droppable/health_orb_sprite/"

        self.animations = {'health_orb': []}

        for animation in self.animations.keys():
            full_path = health_orb_path + animation
            self.animations[animation] = support_folder(full_path)



    def update(self):
        pass