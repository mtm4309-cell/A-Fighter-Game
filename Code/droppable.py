import pygame, random
from support import import_folder
class Droppable():
    def __init__(self,screen):

        # Getting dimensions of the user screen
        self.screen = screen
        self.MAX_WIDTH = self.screen.get_width()
        self.MAX_HEIGHT = self.screen.get_height()

        self.set_health_orb_spawn_point()

        self.health_orb_attributes = {'Duration': 5000, 'Health Boost': 20}
        self.duration_for_health_orb_to_remain = self.health_orb_attributes['Duration']
        self.frame_index = 0
        self.animation_speed = 0.15
        self.is_health_orb_collected = False
        self.last_player_health = None


        original_health_orb_image = pygame.image.load("Sprites/droppable/health_orb/frame-001.png").convert_alpha()
        self.image = pygame.transform.scale(original_health_orb_image, (150, 150))
        self.rect = self.image.get_rect(topleft=self.point_at_which_health_orb_will_spawn)
        self.rect.inflate_ip(-50, 0)

        self.import_health_orb_assets()
        self.font = pygame.font.Font("UI related/FONTS/rainyhearts.ttf", 40)
        self.time_elapsed = pygame.time.get_ticks()
        self.health_orb_timer_started = False

    def import_health_orb_assets(self):
        # Load the frame sequence from the same directory as the orb image.
        health_orb_path = "Sprites/droppable/health_orb/"
        self.animations = {'health_orb': import_folder(health_orb_path)}

    def set_health_orb_spawn_point(self):
        self.x_coordinate_at_which_health_orb_will_spawn = random.randint(0, max(0, self.MAX_WIDTH - 150))
        self.point_at_which_health_orb_will_spawn = (
            self.x_coordinate_at_which_health_orb_will_spawn,
            self.MAX_HEIGHT // 2,
        )


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
            if not self.health_orb_timer_started: # --> Ensures that for each appearance of the health orb, the timer starts only once, without any baggage from the previous instance.
                self.time_elapsed = pygame.time.get_ticks()
                self.health_orb_timer_started = True
            if pygame.time.get_ticks() - self.time_elapsed >= self.duration_for_health_orb_to_remain:
                return False

            self.animate_health_orb()
            remaining_duration = max(0, self.duration_for_health_orb_to_remain - (pygame.time.get_ticks() - self.time_elapsed))
            duration_text = self.font.render(f"{remaining_duration / 1000:.1f}", True, (255, 255, 255))
            self.screen.blit(duration_text, (self.rect.x + 50, self.rect.y - 30))
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
        self.set_health_orb_spawn_point()
        self.rect.topleft = self.point_at_which_health_orb_will_spawn
        self.time_elapsed = pygame.time.get_ticks()
        self.health_orb_timer_started = True
        self.frame_index = 0

    def droppable_update_with_player(self,player):
        
        current_health = player.health_being_updated
        if self.last_player_health is None:
            self.last_player_health = current_health
        elif current_health != self.last_player_health:
            if self.is_health_orb_collected:
                self.is_health_orb_collected = False
                player.has_player_collected_health_orb = False
                self.respawn_of_health_orb()
            if pygame.time.get_ticks() - self.time_elapsed >= self.duration_for_health_orb_to_remain:            
                player.has_player_collected_health_orb = False
                self.is_health_orb_collected = False
                while not current_health == self.last_player_health:
                    self.respawn_of_health_orb()
                    break

            self.last_player_health = current_health

        if self.is_health_orb_collected:
            return

            
        if self.check_if_health_orb_is_collected(player):
            self.give_player_health_boost(player)
        
        