import pygame, random
from support import import_folder
class Droppable():
    def __init__(self,screen):

        # Getting dimensions of the user screen
        self.screen = screen
        self.MAX_WIDTH = self.screen.get_width()
        self.MAX_HEIGHT = self.screen.get_height()

        self.x_coordinate_at_which_health_orb_will_spawn = random.randint(0, max(0, self.MAX_WIDTH - 150))

        self.point_at_which_health_orb_will_spawn = (self.x_coordinate_at_which_health_orb_will_spawn, self.MAX_HEIGHT//2)

        self.health_orb_attributes = {'Duration': 5000, 'Health Boost': 20}
        self.duration_for_health_orb_to_remain = self.health_orb_attributes['Duration']
        self.frame_index = 0
        self.animation_speed = 0.15
        self.is_health_orb_collected = False
        self.last_player_health = None


        original_health_orb_image = pygame.image.load("Sprites/droppable/health_orb/frame-001.png").convert_alpha()
        self.image = pygame.transform.scale(original_health_orb_image, (150, 150))
        self.rect = self.image.get_rect(topleft=self.point_at_which_health_orb_will_spawn)

        self.import_health_orb_assets()

        self.time_elapsed = pygame.time.get_ticks()

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

                if self.is_health_orb_collected:
                    self.frame_index = 0

            self.image = pygame.transform.scale(animation[int(self.frame_index)], (100, 100))
        
        self.screen.blit(self.image, self.rect)
    
    def check_if_health_orb_is_collected(self,player):

        if player.health_being_updated == 100 or player.health_being_updated < 30:
            return False

        else:
            if pygame.time.get_ticks() - self.time_elapsed >= self.duration_for_health_orb_to_remain:
                return False

            self.animate_health_orb()
            if not self.is_health_orb_collected and player.rect.colliderect(self.rect):
                return True

        return False
        
    def give_player_health_boost(self,player):
        if player.health_being_updated < 100 and player.health_being_updated > 30:
            player.health_being_updated += self.health_orb_attributes['Health Boost']
            player.player_heal.play()
            if player.health_being_updated > 100:                
                player.health_being_updated = 100


            self.is_health_orb_collected = True
            player.has_player_collected_health_orb = True
            self.frame_index = 0
        print(f"Player health after collecting health orb: {player.health_being_updated}")        


    def respawn_of_health_orb(self):
        self.x_coordinate_at_which_health_orb_will_spawn = random.randint(0, max(0, self.MAX_WIDTH - 150))
        self.point_at_which_health_orb_will_spawn = (
            self.x_coordinate_at_which_health_orb_will_spawn,
            self.MAX_HEIGHT // 2,
        )
        self.rect.topleft = self.point_at_which_health_orb_will_spawn
        self.time_elapsed = pygame.time.get_ticks()
        self.frame_index = 0

    
    def droppable_update_with_player(self,player):
        current_health = player.health_being_updated
        if self.last_player_health is None:
            self.last_player_health = current_health
        elif current_health != self.last_player_health:
            self.respawn_of_health_orb()
            self.is_health_orb_collected = False
            player.has_player_collected_health_orb = False
            self.last_player_health = current_health

        if self.is_health_orb_collected:
            return

        if pygame.time.get_ticks() - self.time_elapsed >= self.duration_for_health_orb_to_remain:            
            player.has_player_collected_health_orb = False
            self.is_health_orb_collected = False
            self.respawn_of_health_orb()

        if self.check_if_health_orb_is_collected(player):
            self.give_player_health_boost(player)
                