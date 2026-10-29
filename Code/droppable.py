import pygame, player, random
from support import import_folder
class droppable():
    def __init__(self,screen):

        # Getting dimensions of the user screen
        self.screen = screen
        self.MAX_WIDTH = self.screen.get_width()
        self.MAX_HEIGHT = self.screen.get_height()

        self.x_coordinate_at_which_health_orb_will_spawn = random.randint(0,self.MAX_WIDTH)

        self.point_at_which_health_orb_will_spawn = (self.x_coordinate_at_which_health_orb_will_spawn, self.MAX_HEIGHT//2)

        self.health_orb_attributes = {'Duration': 5000, 'Health Boost': 20}

        self.frame_index = 0
        self.animation_speed = 0.15
        self.is_health_orb_collected = False


        original_health_orb_image = pygame.image.load("Sprites/droppable/health_orb/frame-001.png").convert_alpha()
        self.image = pygame.transform.scale(original_health_orb_image, (150, 150))
        self.rect = self.image.get_rect(topleft=self.point_at_which_health_orb_will_spawn)

        self.import_health_orb_assets()


    def import_health_orb_assets(self):
        # Load the frame sequence from the same directory as the orb image.
        health_orb_path = "Sprites/droppable/health_orb/"
        self.animations = {'health_orb': import_folder(health_orb_path)}


    def animate_health_orb(self):
        animation = self.animations['health_orb']
        if animation:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0

            if self.frame_index >= 8 and self.frame_index <= 10 and not self.is_health_orb_collected:
                self.frame_index = 8


            self.image = pygame.transform.scale(animation[int(self.frame_index)], (100, 100))

        self.screen.blit(self.image, self.rect)
    
    def check_if_health_orb_is_collected(self,player):

        if player.health_being_updated == 100 or player.health_being_updated < 30:
            return False

        else:
            self.animate_health_orb()
            if not self.is_health_orb_collected and player.rect.colliderect(self.rect):
                return True

        return False
        
    def give_player_health_boost(self,player):
        if player.health_being_updated < 100 and player.health_being_updated > 30:
            player.health_being_updated += self.health_orb_attributes['Health Boost']
            
            if player.health_being_updated > 100:                
                player.health_being_updated = 100


            self.is_health_orb_collected = True
            
        print(f"Player health after collecting health orb: {player.health_being_updated}")        

        self.is_health_orb_collected = False

    
    def droppable_update_with_player(self,player):
        if self.is_health_orb_collected:
            return

        if self.check_if_health_orb_is_collected(player):
            self.give_player_health_boost(player)