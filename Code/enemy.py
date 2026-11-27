import math
import pygame, random
from support import import_folder, load_image, load_sound
from player import Player
class Enemy():
    def __init__(self, health, damage,speed, level,screen):
        self.health = health
        self.damage = damage
        self.level = level
        self.speed = speed

        self.screen = screen
        self.MAX_WIDTH = self.screen.get_width() # (x cordinate)

        self.enemy_x = 200
        self.enemy_y = 300
        self.status = ''
        self.frame_index = 0
        self.animation_speed = 0.15

        self.enemy_health = 100
        self.has_been_hit = False
        self.knockback_velocity = pygame.math.Vector2() # --> Initially a zero vector

        # [Loading assets handled by support.py to ensure that the game loads faster and more efficiently]
        

        original_image = load_image("Sprites/enemy_sprite/east_idle/east.png")


        self.alpha = 255 # Helps in the opaqueness of the text.
        self.frame_speed = 10
        self.damage_text_y_offset = 0 # Will help in causing the text to go up as it fades, making the animation-like effect more smoother.
        self.damage_text = None

        
        self.image = pygame.transform.scale(original_image, (500,500))
        self.pos = pygame.math.Vector2(self.enemy_x,self.enemy_y)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.hitbox = self.rect.inflate(-400,-350)

        self.attack_radius = 60 # Kicking animation is played here
        self.scythe_radius = 400  # For the scythe to be thrown
        self.kick_attributes = {'Damage': 10,'Knockback': 60, 'Knockback_Multiplier': 0.35}
        self.scythe_attributes = {'Damage': 15, 'Knockback': 45, 'Knockback_Multiplier': 0.3}
        self.notice_radius = 700 # --> Enemy would start moving immediately, and gives the game a more active feel

        self.is_kick_sound_played = False
        self.is_scythe_sound_played = False
        self.scythe_attack_cooldown = 2000
        self.last_scythe_attack_time = pygame.time.get_ticks() - self.scythe_attack_cooldown # To give some time between subsequent attacks
        self.is_scythe_attacking = False # For the enemy
        self.scythe_was_thrown = False # For damage registration onto player
        self.scythe_target_at_launch = pygame.math.Vector2() # A vector quantity, which is set towards the player
        self.scythe_in_flight = False
        self.scythe_start_position = pygame.math.Vector2() # This would be where the enemy is
        self.scythe_target_position = pygame.math.Vector2() # Where the player is
        self.scythe_direction = pygame.math.Vector2()  # Calculated when the scythe is thrown
        self.scythe_facing_left = False
        self.scythe_started_at = 0
        self.scythe_flight_duration = 0
        self.scythe_frame_index = 0
        self.scythe_rect = pygame.Rect(0, 0, 54, 54)


    # --- START OF ASSETS --- # 
        self.kick = load_sound("Sound Effects/kick.mp3")
        self.enemy_laugh = load_sound("Sound Effects/enemy_laugh.mp3")
        self.enemy_get_hurt = load_sound("Sound Effects/enemy_get_hurt.mp3")
        self.enemy_get_hurt.set_volume(0.1)
        self.scythe_sound_effect = load_sound("Sound Effects/scythe_being_thrown.mp3")


    # --- END OF ASSETS --- #

        self.import_enemy_assets()

    def import_enemy_assets(self):
        enemy_path = "Sprites/enemy_sprite/"

        self.animations = {'east_idle': [], 'east_walk':[], 'east_attack':[], 'east_hurt':[], 'east_scythe_attack' : [], 'east_death' : [],
                           'west_idle': [], 'west_walk': [], 'west_attack' : [], 'west_hurt': [], 'west_scythe_attack' : [], 'west_death' : []}

        self.attack_animations ={'scythe':[]}

        for animation in self.animations.keys():
            full_path_1 = enemy_path + animation
            self.animations[animation] = import_folder(full_path_1)

        for attack_animation in self.attack_animations.keys(): # Bringing in the attack of the scythe
            full_path_2 = enemy_path + attack_animation
            self.attack_animations[attack_animation] = import_folder(full_path_2)

    def get_player_distance_directions(self,player):
        
        enemy_vector= pygame.math.Vector2(self.rect.center)
        
        player_vector = pygame.math.Vector2(player.rect.center)
        
        distance = (player_vector-enemy_vector).magnitude() #---> Will be important to determine whether the player is within the notice radius or attack radius of the enemy, and then the enemy will react accordingly
        

        if distance > 0:
            direction =(player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2((0,0))

        if direction.x > 0:
            horizontal_pos = 'east'
        elif direction.x < 0:
            horizontal_pos = 'west'
        else:
            horizontal_pos = 'east' if 'east' in self.status else 'west'

        return (distance, direction, horizontal_pos)

    def get_status(self,player):
        distance,direction,horizontal_pos = self.get_player_distance_directions(player)
        if self.enemy_health > 0:  
            if self.has_been_hit:
                self.is_scythe_attacking = False
                self.scythe_in_flight = False
                state = '_hurt'
                self.direction = pygame.math.Vector2()
                self.animation_speed = 0.20
            
            elif self.is_scythe_attacking: # Causes the relevant animation to be played
                state = '_scythe_attack'
                self.direction = pygame.math.Vector2()
            
            elif distance <= self.attack_radius and distance < self.notice_radius:
                state = '_attack'
                self.direction = direction
            
            elif distance <= self.scythe_radius and distance > self.attack_radius:
                # Start a scythe attack when the cooldown has elapsed.
                if pygame.time.get_ticks() - self.last_scythe_attack_time >= self.scythe_attack_cooldown:
                    self.last_scythe_attack_time = pygame.time.get_ticks()

                    if random.choice((True, False)) == True: # 50/50 chance of either enemy walking, or using scythe attack. 
                        self.is_scythe_attacking = True
                        self.scythe_was_thrown = False
                        self.scythe_target_at_launch = pygame.math.Vector2(player.hitbox.center)
                        state = '_scythe_attack'
                        self.direction = pygame.math.Vector2()
                    else:
                        state = '_walk'
                        self.direction = direction
            
                else:
                    # Close the distance while waiting for the scythe cooldown.
                    state = '_walk' # Once the scythe attack is done, the enemy returns to walking.
                    self.direction = direction
                # The scythe range is separate from the kick attack, so reset kick sound state.
                self.is_kick_sound_played = False
            
            
            elif distance <= self.notice_radius: #---> When the player has only entered inside the notice radius, the enemy will start moving towards the player
                state = '_walk'

                self.is_kick_sound_played = False #---> #This ensures that when the player runs away from the enemy after invading the attack radius, the sound effect will stop.
                self.direction = direction 
            
            else:
                state = '_idle' # ---> If no radii has been entered, the enemy will remain idle and not move towards the player
                self.direction = pygame.math.Vector2(0, 0)

        else:
            state = '_death'


        new_status = horizontal_pos + state

        if new_status != self.status:
            self.frame_index = 0
            self.is_kick_sound_played = False # ---> This ensures that when the player runs away from the enemy after invading the attack radius, the sound effect will stop.

        self.status = new_status

    def get_actions(self,player):
        if 'walk' in self.status:
            self.direction = self.get_player_distance_directions(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()        

        self.pos.x +=self.direction.x * speed
        
        self.pos += self.knockback_velocity # --> This will happen only when the enemy is hit by the blast, 
        self.knockback_velocity *= 0.8 # --> Creates a deceleration effect, making things look smooth, this works as the self.knockback_velocity is changing when the enemy is hit by the blast.
        
        if self.knockback_velocity.length_squared() < 0.01: # --> A threshold to determine when to stop knockback effect.
            self.knockback_velocity.update(0, 0)
        
        self.rect.topleft = self.pos

        self.hitbox.center = self.rect.center


    def animate(self):
        animations = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animations):
            self.frame_index = 0
            self.is_kick_sound_played = False # ---> This ensures that the sound effect will only play once per attack animation, and not multiple times during the same animation cycle
            if 'scythe_attack' in self.status:
                self.is_scythe_attacking = False

        if 'hurt' in self.status and self.frame_index >= len(animations) - 1: # --> Checks for when one loop of the hurt animation is played so that the hurting animation stops.
            self.has_been_hit = False
            self.animation_speed = 0.15

        if 'scythe_attack' in self.status:
            if int(self.frame_index) >= 8 and not self.scythe_was_thrown: # The 8th frame is chosen, as that seems to be the most visibly appropriate point for the scythe to be thrown.
                self.is_scythe_sound_played = True
                self.throw_scythe()
        elif 'attack' in self.status: ## ---> Selecting a specific frame of the attack naimation for sound effect to play.
            if int(self.frame_index) == 5 and self.is_kick_sound_played == False: # ---> The self frame index at which the sound is playeed has changed from '2' to '5' so that the sound effect is played at the point of contact between the kick and the player.
                self.is_kick_sound_played = True
                self.sound_effects()


        self.image = animations[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (200,200))
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def throw_scythe(self): # Sets up the relevant coordinates for where the scythe is thrown and lands
        self.scythe_was_thrown = True
        self.scythe_in_flight = True
        self.scythe_facing_left = 'west' in self.status
        
        # Save the projectile's launch and landing positions.
        self.scythe_start_position = pygame.math.Vector2(self.rect.center)
        
        self.scythe_target_position = self.scythe_target_at_launch.copy() # This is fully understood at Line 130
        
        # Calculate the travel time based on the distance to the target.
        self.scythe_direction = self.scythe_target_position - self.scythe_start_position
        
        distance = self.scythe_direction.length()
        
        self.scythe_flight_duration = max(350, distance / 700 * 1000) # To Convert seconds to milliseconds for pygame ticks.
        
        # Reset the flight timer and animation for this throw.
        self.scythe_started_at = pygame.time.get_ticks()
        
        self.scythe_frame_index = 0
        
        # Start the projectile at the enemy's position.
        self.scythe_rect.center = self.scythe_start_position

    def update_scythe_projectile(self, target_position):
        if not self.scythe_in_flight:
            return

        self.scythe_target_position = pygame.math.Vector2(target_position) # This is given in the player_damage_health function, allowing for for this position to be updated based upon where the player is.
        self.scythe_direction = self.scythe_target_position - self.scythe_start_position

        elapsed = pygame.time.get_ticks() - self.scythe_started_at # To see how much time has gone by since the scythe is thrown.
        progress = min(elapsed / self.scythe_flight_duration, 1) # This is capped at 1, so that it doesn't go beyond target.
        position = self.scythe_start_position + self.scythe_direction * progress # To get it's current position, we add to its start position the product of multiplying the direction of the scythe with its progress of movement.
        position.y -= math.sin(math.pi * progress) * 100  # To give the scythe's height an arc-like effect. (Its Max Height will be 100 pixels above its straight line path, with its height varying throughout the start and end of movement)
        self.scythe_rect.center = round(position.x), round(position.y) # We need this to find point of collision between player and scythe.

        if elapsed > self.scythe_flight_duration + 100: # Keep the scythe active for a brief period of time to register the collision check.
            self.scythe_in_flight = False

    def draw_scythe_projectile(self):
        if not self.scythe_in_flight:
            return

        # Making the image of the scythe.
        animations = self.attack_animations['scythe']
        self.scythe_frame_index = (self.scythe_frame_index + self.animation_speed) % len(animations)
        image = pygame.transform.scale(animations[int(self.scythe_frame_index)], (100, 100))
        if self.scythe_facing_left:
            image = pygame.transform.flip(image, True, False)
        self.screen.blit(image, image.get_rect(center=self.scythe_rect.center))

    def enemy_health_bar(self):

        bar_width = 200 #---> Defining the elements for the health bar
        bar_height = 20

        bar_x = self.rect.x + (self.rect.width - bar_width) // 2 #--> Centering the health bar above the enemy sprite
        bar_y = self.rect.y - bar_height - 10 #--> Positioning the health bar above the enemy sprite with a 10-pixel gap

        health_ratio = self.enemy_health / self.health #--> Calculating the ratio of the enemy's current health to its maximum health
        current_bar_width = bar_width * health_ratio #--> Calculating the current width of the health bar based on the enemy's current health

        #1) Drawing the red background of the health bar
        back_health_bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (20, 18, 20), back_health_bar_rect) # ---> Obsidian Charcoal Colour

        #2) Drawing the green foreground of the health bar
        if current_bar_width > 0:
            fore_health_bar_rect = pygame.Rect(bar_x, bar_y, current_bar_width, bar_height)
            pygame.draw.rect(self.screen, (192, 57, 43), fore_health_bar_rect)  # ---> Blood Ember Colour 

        #3) Drawing the border of the health bar 
        pygame.draw.rect(self.screen, (0, 0, 0), back_health_bar_rect, 2) # ---> Pitch Black Colour

    def sound_effects(self):
        if self.is_kick_sound_played and not pygame.mixer.Channel(3).get_busy():
            self.animation_speed = 0.175
            pygame.mixer.Channel(3).play(self.kick)
            self.is_kick_sound_played = False
        
        if not 'attack' in self.status and not pygame.mixer.Channel(4).get_busy():
            if self.enemy_health > 0: # Only played when the enemy is alive, and not dead.
                pygame.mixer.Channel(4).play(self.enemy_laugh) if random.randint(1, 720) == 1 else None  # Play the laugh sound effect with a 1 in every 720 chances, the number chosen is arbritary.

        if self.is_scythe_sound_played and not pygame.mixer.Channel(5).get_busy():
            pygame.mixer.Channel(5).play(self.scythe_sound_effect)
            self.is_scythe_sound_played = False
    
    def enemy_get_hurt_by_blast(self,player):
        # Detect the collision as soon as the blast overlaps the enemy.
        if player.collision_of_blast_with_enemy(self):
            if self.has_been_hit:
                return
            self.has_been_hit = True
                   
            if player.blast_type == "blue_blast":
                damage = player.blue_blast_attributes["Damage"]
                distance_by_which_enemy_goes_back = player.blue_blast_attributes["Distance_by_which_enemy_goes_back"]
                multiplier_for_enemy_knockback = player.blue_blast_attributes["Multiplier_for_enemy_knockback"]
            elif player.blast_type == "purple_blast":
                damage = player.purple_blast_attributes["Damage"]
                distance_by_which_enemy_goes_back = player.purple_blast_attributes["Distance_by_which_enemy_goes_back"]
                multiplier_for_enemy_knockback = player.purple_blast_attributes["Multiplier_for_enemy_knockback"]
            else:
                damage = 0
                distance_by_which_enemy_goes_back = 0

            if self.rect.centerx != player.rect.centerx: # --> Knockback effect will only be applied if the enemy and player are not perfectly aligned vertically.
                if self.rect.centerx > player.rect.centerx: # --> This stops the glitch where the enemy goes upwards.
                    knockback_direction = 1  
                else:
                    knockback_direction = -1
            else: # --> If the enemy and player are perfectly aligned vertically, we determine what direction the enemy should be knocked back based on its current status (facing east or west).
                if 'east' in self.status:
                    knockback_direction = -1
                else:
                    knockback_direction = 1
            
            self.knockback_velocity.x += knockback_direction * distance_by_which_enemy_goes_back * multiplier_for_enemy_knockback 
            # --> By how much the knockback velocity is increased depends on the distance by which the enemy goes back and the multiplier for enemy knockback. The multiplier is used to adjust the knockback effect based on the blast type.
                
            self.enemy_health = self.enemy_health - damage

            self.damage_text = player.level_font.render(str(damage), False,  '#dfce67')
            self.alpha = 255
            self.damage_text_y_offset = 0
            
            print(f"Enemy health after blast: {self.enemy_health}")
            self.enemy_get_hurt.play()  # Play the sound effect when the enemy gets hurt

    def enemy_hurt_by_sword(self,player):
        damage = player.sword_attributes['Damage']
        knockback = player.sword_attributes['Distance_by_which_enemy_goes_back']
        knockback_multipler = player.sword_attributes['Multiplier_for_enemy_knockback']

        if player.sword_attack(self):
            if self.has_been_hit:
                return  
            self.has_been_hit = True

            if self.rect.centerx != player.rect.centerx: # --> Knockback effect will only be applied if the enemy and player are not perfectly aligned vertically.
                if self.rect.centerx > player.rect.centerx: # --> This stops the glitch where the enemy goes upwards.
                    knockback_direction = 1  
                else:
                    knockback_direction = -1
            else: # --> If the enemy and player are perfectly aligned vertically, we determine what direction the enemy should be knocked back based on its current status (facing east or west).
                if 'east' in self.status:
                    knockback_direction = -1
                else:
                    knockback_direction = 1
            
            self.knockback_velocity.x += knockback_direction * knockback *knockback_multipler
            # --> By how much the knockback velocity is increased depends on the distance by which the enemy goes back and the multiplier for enemy knockback. The multiplier is used to adjust the knockback effect based on the blast type.
                
            self.enemy_health = self.enemy_health - damage


            self.damage_text = player.level_font.render(str(damage), False, '#dfce67')
            self.alpha = 255
            self.damage_text_y_offset = 0
            print(f"Enemy health after blast: {self.enemy_health}")
            self.enemy_get_hurt.play()  # Play the sound effect when the enemy gets hurt

    def enemy_stay_within_screen_boundaries(self):
        # Useful especially when the enemy is hit by the blast and is knocked back, to ensure it doesn't go off-screen.
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > self.MAX_WIDTH - self.rect.width:
            self.pos.x = self.MAX_WIDTH - self.rect.width   
          
    def update(self):
        self.enemy_stay_within_screen_boundaries()
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.move(self.speed)
        self.animate()
        self.draw_scythe_projectile()
        self.sound_effects()
        self.enemy_health_bar()
        pygame.draw.rect(self.screen,"green", self.rect,1)
        pygame.draw.rect(self.screen,"blue", self.hitbox,1)
        if self.damage_text is not None:
            self.alpha = max(0,self.alpha - self.frame_speed) # Text fades out slowly
            self.damage_text.set_alpha(self.alpha)
            self.screen.blit(self.damage_text, (self.rect.x, (self.rect.y - 30))) # -30 for the text to be up at first, and then the offset makes it go further up.
            if self.alpha == 0:
                self.hurt_text = None


    def enemy_update(self,player):
        self.get_status(player)
        self.get_actions(player)
        self.enemy_get_hurt_by_blast(player) 
        self.enemy_hurt_by_sword(player)