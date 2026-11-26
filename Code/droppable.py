import pygame, random
from support import import_folder, load_image
class Droppable():
    def __init__(self,screen):

        # Getting dimensions of the user screen
        self.screen = screen
        self.MAX_WIDTH = self.screen.get_width()
        self.MAX_HEIGHT = self.screen.get_height()

        self.font = pygame.font.Font("UI related/FONTS/rainyhearts.ttf", 40)
        self.time_elapsed = pygame.time.get_ticks()


        # -- INITIALISATION OF HEALTH ORB -- #
        
        self.set_health_orb_spawn_point()

        self.health_orb_attributes = {'Duration': 5000, 'Health Boost': 20}
        self.duration_for_health_orb_to_remain = self.health_orb_attributes['Duration']
        self.frame_index = 0
        self.animation_speed = 0.15
        self.is_health_orb_collected = False
        self.last_player_health = None
        self.health_gain_text = None

        self.alpha = 255
        self.frame_speed = 10
        self.health_gain_text_offset_y = 0

        # [Loading assets handled by support.py to ensure that the game loads faster and more efficiently]
        

        original_health_orb_image = load_image("Sprites/droppable/health_orb/frame-001.png")
        self.health_image = pygame.transform.scale(original_health_orb_image, (150, 150))
        self.health_rect = self.health_image.get_rect(topleft=self.point_at_which_health_orb_will_spawn)
        self.health_rect.inflate_ip(-50, 0)
        self.health_orb_timer_started = False
        self.health_orb_available = True

        self.import_health_orb_assets()

        # -- END OF INITIALISATION OF HEALTH ORB -- #


        # -- INITIALISATION OF BANANA PEEL -- #

        original_banana_peel_image = pygame.image.load("Sprites/droppable/banana_peel/frame_001.png").convert_alpha()
        self.banana_peel_image = pygame.transform.scale(original_banana_peel_image, (150, 150))
        self.banana_peel_rect = self.banana_peel_image.get_rect()

        self.set_banana_peel_spawn_point()

        self.banana_available = True # Always must be False by default, else it will be annoying at the start of the game.
        self.banana_peel_finished = False

        self.banana_peel_attributes = {'Duration': 4500, 'Slipping Effect': 30}
        self.banana_frame_index = 0
        self.banana_peel_phase = "active"
        self.banana_peel_active_since = None
        self.banana_respawn_at = None

        self.import_banana_peel_assets()

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

            self.health_image = pygame.transform.scale(animation[int(self.frame_index)], (100, 100))
        
        self.screen.blit(self.health_image, self.health_rect)
    
    def check_if_health_orb_is_collected(self,player):

        if player.health_being_updated == 100 or player.health_being_updated < 30:
            return False
        if not self.health_orb_available:
            return False

        else:
            current_ticks = pygame.time.get_ticks()
            if not self.health_orb_timer_started: # Start a fresh timer for each orb instance.
                self.time_elapsed = current_ticks
                self.health_orb_timer_started = True
            elapsed = current_ticks - self.time_elapsed
            if elapsed >= self.duration_for_health_orb_to_remain:
                return False # --> Once time is overdue, the health orb will disappear 

            self.animate_health_orb()
            remaining_duration = max(0, self.duration_for_health_orb_to_remain - elapsed) # Gives the player how much time remains to collect health orb
            duration_text = self.font.render(f"{remaining_duration / 1000:.1f}s", True, (255, 255, 255))
            self.screen.blit(duration_text, (self.health_rect.x + 50, self.health_rect.y - 50)) # Display the remaining time.
            if not self.is_health_orb_collected and player.rect.collidepoint(self.health_rect.center): # Ensures a more accurate health orb colliding detection.
                return True

        return False
        
    def give_player_health_boost(self,player):
        if (player.health_being_updated < 100 ) and self.frame_index >=8 : # The self.frame_index condition is placed as the animation of the health orb is complete by around the 8th frame, whereas the frames before is the animation to bring forth the health orb.
            player.health_being_updated += self.health_orb_attributes['Health Boost']
            player.player_heal.play()

            player.has_player_collected_health_orb = True
            self.alpha = 255
            self.health_gain_text_offset_y = 0
            self.health_gain_text = player.level_font.render(f"{self.health_orb_attributes['Health Boost']}", False, "#48ba79") # Text to be displayed

            if player.health_being_updated > 100:                
                player.health_being_updated = 100

            self.is_health_orb_collected = True
            self.frame_index = 0

        print(f"Player health after collecting health orb: {player.health_being_updated}")        

    def respawn_of_health_orb(self):
        self.health_orb_available = random.choice((True,False))
        self.health_orb_timer_started = False
        self.frame_index = 0

        if self.health_orb_available: # 50/50 Chance for the health orb to spawn.
            self.set_health_orb_spawn_point()
            self.health_rect.topleft = self.point_at_which_health_orb_will_spawn

    def health_orb_update_with_player(self,player):
        #pygame.draw.rect(self.screen ,'green',self.health_rect ,2) # For debugging
        
        if player.has_player_collected_health_orb and self.health_gain_text is not None: # Text is displayed here, where it is not limited by irrelevant conditions.
            self.alpha = max(0,self.alpha - self.frame_speed)
            self.health_gain_text.set_alpha(self.alpha)
            self.health_gain_text_offset_y +=self.frame_speed/10
            self.screen.blit(self.health_gain_text,(player.rect.x,player.rect.y - 30-self.health_gain_text_offset_y))
        else:
            self.health_gain_text = None

        if self.point_at_which_health_orb_will_spawn != player.player_x or self.point_at_which_health_orb_will_spawn == (player.player_x -500) or self.point_at_which_health_orb_will_spawn == (player.player_x + 500) :
            current_health = player.health_being_updated
            if self.last_player_health is None:
                self.last_player_health = current_health
            elif current_health != self.last_player_health:
                if self.is_health_orb_collected:
                    self.is_health_orb_collected = False
                    self.respawn_of_health_orb()
                if pygame.time.get_ticks() - self.time_elapsed >= self.duration_for_health_orb_to_remain:            
                    self.is_health_orb_collected = False
                    while not current_health == self.last_player_health:
                        self.respawn_of_health_orb()
                        break

                self.last_player_health = current_health

            if self.is_health_orb_collected:
                return

                
            if self.check_if_health_orb_is_collected(player):
                self.give_player_health_boost(player)
        
    # -- END OF HEALTH ORB RELATED CODE -- #

    # -- START OF BANANA PEEL CODE -- #

    def import_banana_peel_assets(self):
        # Load the frame sequence from the same directory as the banana peel image.
        banana_peel_path = "Sprites/droppable/banana_peel/"
        self.banana_peel_animations = {'banana_peel': import_folder(banana_peel_path)}

    def animate_banana_peel(self):
        animation = self.banana_peel_animations['banana_peel'] # Loading the relevant frames
        if self.banana_peel_finished or not animation:
            return None

        # Draw each frame before going to the next frame.
        current_frame = int(self.banana_frame_index)
        self.banana_peel_image = pygame.transform.scale(animation[current_frame], (125, 125))
        self.screen.blit(self.banana_peel_image, self.banana_peel_rect)

        # Keep the active animation on its final frame; let the outro advance.
        if self.banana_peel_phase == "active":
            self.banana_frame_index = min(8, self.banana_frame_index + self.animation_speed) # Keeps the peel locked at the 9th image.
        else: # At the 'outro' part where the animation will be complete.
            self.banana_frame_index += self.animation_speed

        return current_frame


    def set_banana_peel_spawn_point(self):
        self.x_coordinate_at_which_banana_peel_will_spawn = random.randint(0, max(0, self.MAX_WIDTH - 150))
        self.point_at_which_banana_peel_will_spawn = (
            self.x_coordinate_at_which_banana_peel_will_spawn,
            self.MAX_HEIGHT // 2,
        )
        self.banana_peel_rect.topleft = self.point_at_which_banana_peel_will_spawn

    def try_banana_peel_respawn(self, current_ticks):
        # Randomly make the peel available again or delay its next appearance.
        self.banana_available = random.choice((True, False))
        if self.banana_available: # Setting up relevant variables for the banana peel to spawn and do its job
            self.banana_peel_finished = False
            self.banana_peel_phase = "active"
            self.banana_frame_index = 0
            self.banana_peel_active_since = None
            self.banana_respawn_at = None
            self.set_banana_peel_spawn_point()
        else: # If false, some time is given before the random.choice function is used again.
            self.banana_respawn_at = (current_ticks + self.banana_peel_attributes['Duration'])

    def banana_peel_update_with_player(self,player): # The actual occurence of the banana peel
        current_ticks = pygame.time.get_ticks()
        #pygame.draw.rect(self.screen ,'yellow',self.banana_peel_rect ,2) # For debugging

        if not self.banana_available: # When false, time is given before the re-rolling of the peel spawning occurs.
            if (self.banana_respawn_at is not None and current_ticks >= self.banana_respawn_at):
                self.try_banana_peel_respawn(current_ticks)
            return

        animation = self.banana_peel_animations['banana_peel'] # In case there are any problems with files.
        if not animation:
            return

        if (self.banana_peel_phase == "active" and self.banana_peel_active_since is not None and current_ticks - self.banana_peel_active_since >= self.banana_peel_attributes['Duration']):
            # If NO collision has occured and so the peel's active time has ended, so continue with the outro frames.
            self.banana_peel_phase = "outro"
            self.banana_frame_index = 9 # This occurs in the animate function.

        if self.banana_peel_phase == "active": # Animation of the first 9 images of the banana peel
            current_frame = self.animate_banana_peel()
            if current_frame is None:
                return  # In case of any errors in fikes.

            # Only active frames can trigger a slip when the player overlaps the peel.
            if 6 <= current_frame <= 8 and self.banana_peel_rect.colliderect(player.hitbox):
                player.apply_slip(self.banana_peel_attributes['Slipping Effect']) # Causing the player to slip
                self.banana_peel_phase = "outro" # Once this collision has occured, the animation will now be complete
                self.banana_frame_index = 9
            
            elif current_frame == 8 and self.banana_peel_active_since is None: 
                self.banana_peel_active_since = current_ticks # To ensure that the relevant timer is set only once, rather than being updated constantly as the image is displayed.
            return 

        if self.banana_frame_index >= len(animation): # Once the animation is complete, the program goes back to respawning the banana peel.
            self.banana_peel_finished = True
            self.try_banana_peel_respawn(current_ticks)
            return

        
        self.animate_banana_peel() # Actual animation of banana peel.



        # -- END OF BANANA PEEL CODE -- #
