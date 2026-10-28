import pygame, player
from support import import_folder
class droppable():
    def __init__(self,screen):

        # Getting dimensions of the user screen
        self.screen = screen
        self.MAX_WIDTH = self.screen.get_width()
        self.MAX_HEIGHT = self.screen.get_height()

        self.health_orb_attributes = {'Duration': 5000, 'Health Boost': 20}

        self.frame_index = 0
        self.animation_speed = 0.15
        self.is_health_orb_collected = False


        original_health_orb_image = pygame.image.load("Sprites/droppable/health_orb/frame-001.png").convert_alpha()
        self.image = pygame.transform.scale(original_health_orb_image, (50, 50))
        self.rect = self.image.get_rect(topleft=(self.MAX_WIDTH//2, self.MAX_HEIGHT//2))

        self.import_health_orb_assets()


    def import_health_orb_assets(self):
        health_orb_path = "Sprites/droppable/health_orb_sprite/"

        self.animations = {'health_orb': []}

        for animation in self.animations.keys():
            full_path = health_orb_path + animation
            self.animations[animation] = import_folder(full_path)


    def animate_health_orb(self):
        animation = self.animations['health_orb']
        if not animation:
            return

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = pygame.transform.scale(animation[int(self.frame_index)], (50, 50))
        self.screen.blit(self.image, (self.MAX_WIDTH//2, self.MAX_HEIGHT//3.0))
    
    def check_if_health_orb_is_collected(self,player):
        if (player.health_being_updated < 100 and player.health_being_updated > 30):
            if player.rect.colliderect(self.rect): 
                self.animate_health_orb()
                self.give_player_health_boost(player)
                return True

        return False

    def give_player_health_boost(self,player):
        if self.check_if_health_orb_is_collected(player):
            if player.health_being_updated < 100 and player.health_being_updated > 30:
                player.health_being_updated += self.health_orb_attributes['Health Boost']
            
            elif player.health_being_updated > 100:
                player.health_being_updated = 100
            
            print(f"Player health after collecting health orb: {player.health_being_updated}")        


    
    def droppable_update_with_player(self,player):
        self.give_player_health_boost(player)
