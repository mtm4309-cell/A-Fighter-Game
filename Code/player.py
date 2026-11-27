import pygame , time
from support import import_folder, load_image, load_sound
import droppable
class Player(pygame.sprite.Sprite):
    def __init__(self, health, speed, level, screen):
    
    # --- START OF STATS --- #  
        self.health = health
        self.speed = speed
        self.level = level
        
    # --- END OF STATS --- #
        global health_being_updated
        self.health_being_updated = 100 # --> This variable changes based on the collisions it experiences against the enemy, it is less than 100 to see a change in health bar

    # --- ASSETS --- #  [Loading assets handled by support.py to ensure that the game loads faster and more efficiently]
        
        original_image = load_image("Sprites/player_sprite/east_idle/east.png")
        self.image = pygame.transform.scale(original_image, (150,150))

        self.when_not_running_image = pygame.transform.scale(load_image("UI related/BACKGROUNDS/when_not_running.png"), (85,85))
        self.when_running_image = pygame.transform.scale(load_image("UI related/BACKGROUNDS/when_running.png"), (85,85))

        level_image = load_image("UI related/BACKGROUNDS/level_template.png")
        self.level_image = pygame.transform.scale(level_image, (385,75))

        self.player_death = load_sound("Sound Effects/player_death.mp3")
        self.player_heal = load_sound("Sound Effects/player_heal.wav")

        self.blue_blast = load_sound("Sound Effects/blue_blast.mp3")
        self.blue_blast_button_not_selected = pygame.transform.scale(load_image("UI related/BUTTONS/blue_blast_button_not_selected.png"), (100,100))
        self.blue_blast_button_selected = pygame.transform.scale(load_image("UI related/BUTTONS/blue_blast_button_selected.png"), (100,100))
        self.blue_blast_explosion_sound_effect = load_sound("Sound Effects/blue_blast_explosion.mp3")

        self.purple_blast = load_sound("Sound Effects/purple_blast.mp3")
        self.purple_blast_button_not_selected = pygame.transform.scale(load_image("UI related/BUTTONS/purple_blast_button_not_selected.png"), (100,100))
        self.purple_blast_button_selected = pygame.transform.scale(load_image("UI related/BUTTONS/purple_blast_button_selected.png"), (100,100))
        self.purple_blast_explosion_sound_effect = load_sound("Sound Effects/purple_blast_explosion.mp3")

        self.sword_button_not_selected = pygame.transform.scale(load_image("UI related/BUTTONS/sword_button_not_selected.png"), (100,100))
        self.sword_button_selected = pygame.transform.scale(load_image("UI related/BUTTONS/sword_button_selected.png"), (100,100))
        self.sword_strike = load_sound("Sound Effects/sword_strike.mp3")

        self.level_font = pygame.font.Font("UI related/FONTS/rainyhearts.ttf",54)
        self.level_box_rect = None
        self.hurt_text = None

        self.getting_hurt_sound_effect = load_sound("Sound Effects/player_getting_hurt.mp3")

        self.alpha = 255 # Helps in the opaqueness of the text.
        self.frame_speed = 10
        self.hurt_text_y_offset = 0 # Will help in causing the text to go up as it fades, making the animation-like effect more smoother.

        self.slip_velocity = pygame.math.Vector2() # Helps us with the banana peel.
        self.slip_until = 0

        self.slip_sound = load_sound("Sound Effects/banana_slip.mp3")

    # --- END OF ASSETS --- #


    # --- DATA FOR SCREEN --- #
        self.screen = screen
        self.MAX_WIDTH = self.screen.get_width() # (x cordinate)
        self.MAX_HEIGHT = self.screen.get_height() # (y cordinate) 
    # --- END OF DATA --- #


    # --- PLAYER MOVEMENT --- #
        self.direction = pygame.math.Vector2() # The arrow that tells system where player wants to go

        self.player_x = 750
        self.player_y = 350

        self.pos = pygame.math.Vector2(self.player_x,self.player_y) #System will exactly remember where player actually is

        self.rect = self.image.get_rect(topleft = self.pos) #The picture frame of the player on the screen

        self.hitbox = self.rect.inflate(-40,-12) #The physics part of the player where collisions will be detected

        self.knockback_velocity = pygame.math.Vector2()

        self.is_jumping = False
        self.jump_height = 40 #---> The reason for changing this value is to ensure that when the player jumps, they don't collide with the enemy and take damage.
        self.jump_speed = self.jump_height
        self.gravity = 3

        self.press_r = False
        self.is_sprinting = False
        self.sprint_speed = self.speed * 2

        self.has_player_collected_health_orb = False
        self.has_player_slipped_on_banana_peel = False
        self.is_player_damaged = False
        
        # -- Attack related variables -- #
        self.blue_blast_attributes = {"Damage": 10, "Speed": 15, "Cooldown": 2500, 'Distance_by_which_enemy_goes_back': 55, 'Multiplier_for_enemy_knockback': 0.25}
        self.purple_blast_attributes = {"Damage": 15, "Speed": 25, "Cooldown": 4000, 'Distance_by_which_enemy_goes_back': 70, 'Multiplier_for_enemy_knockback': 0.45}
        self.sword_attributes = {"Damage": 6, 'Distance_by_which_enemy_goes_back':40, 'Multiplier_for_enemy_knockback': 0.20}
        
        self.is_player_blast_attacking = False
        self.is_blue_blast_selected = False #--- > Will Later help us to see which blast attack the player selects, and then playing its respective animation and sound effect.
        self.is_purple_blast_selected = False 
        self.is_blast_released = False
        self.last_blast_time = 0 # --> Assigned later
        self.blast_cooldown = 0 # --> Assigned later
        self.blast_velocity = 0 # --> Assigned later
        self.blast_key_was_down = False

        self.blast_frame_index = 0
        self.blast_animation_speed = 0.10
        self.blast_x = self.player_x
        self.blast_y = self.player_y
        self.blast_facing_right = True
        self.blast_direction = None # --> The direction in which the attack animation moves across the screen, this is to be used in the future when we implement the attack animations to move across the screen
        self.blast_type = None

        self.is_explosion_active = False
        self.explosion_frame_index = 0
        self.explosion_x = 0
        self.explosion_y = 0

        self.blast_rect = pygame.Rect(self.blast_x, self.blast_y, 150, 150)

        self.is_sword_selected = False # --> Checks if button was pressed
        self.sword_key_was_down = False 
        self.sword_hit_frame = 4 # --> The frame at which damage to enemy is registered.
        self.sword_hit_registered = False # --> Helps to register damage onto enemy

        self.is_player_alive = True

    # --- END OF PLAYER MOVEMENT --- #

    # --- PLAYER ANIMATION --- #
        self.status = 'east'
        self.frame_index = 0
        self.animation_speed = 0.15

    # --- END OF PLAYER ANIMATION --- #

        self.clock = pygame.time.Clock()

        self.import_player_assets()


    def import_player_assets(self):
        character_path = "Sprites/player_sprite/"
        self.animations = {'east':[], 'west': [], 
                           'east_idle': [], 'west_idle':[], 
                           'east_death': [], 'west_death': [],
                           'east_attack':[], 'west_attack':[],
                           'east_sword_attack':[], 'west_sword_attack':[],
                           'east_heal': [], 'west_heal': [],
                           'east_hurt': [], 'west_hurt': []}

        self.blast_animations = {'blue_blast': [], 'blue_blast_explosion': [],
                                 'purple_blast': [], 'purple_blast_explosion': []}

        for animation in self.animations.keys():
            full_path_1 = character_path + animation
            self.animations[animation] = import_folder(full_path_1)

        for blast_animation_name in self.blast_animations.keys():
            full_path_2 = character_path + blast_animation_name
            self.blast_animations[blast_animation_name] = import_folder(full_path_2)

    def input(self):
        keys = pygame.key.get_pressed()

        if self.has_player_slipped_on_banana_peel: # Restricting movement for when player has slipped on banana peel
            self.direction.x = 0
            self.direction.y = 0
            return

        # HURT ANIMATION NOT CONSIDERED TO STOP GLITCHES, AND GIVES THE PLAYER MORE FREEDOM
        if (not 'heal' in self.status) and (not '_sword_attack' in self.status) and (self.has_player_slipped_on_banana_peel == False): #--> The player cannot move when they are healing, sword_attack, or if they have slipped, as it is a special animation that should not be interrupted.
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'east'
                self.blast_facing_right = True
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'west'
                self.blast_facing_right = False
            else:
                self.direction.x = 0

            if pygame.KEYDOWN:
                if keys[pygame.K_SPACE]:
                    self.is_jumping = True
        
                if keys[pygame.K_r] and self.press_r == False:
                    if self.is_sprinting == False:
                        self.speed = self.sprint_speed
                        self.animation_speed = 0.25
            
                        self.is_sprinting = True
                
                else:
                    self.speed = self.sprint_speed / 2
                    self.animation_speed = 0.15
                    self.is_sprinting = False
            else:
                self.speed = self.sprint_speed /2
                self.animation_speed = 0.15
                self.is_sprinting = False
                
            if self.is_jumping == True:
                self.pos.y -= self.jump_speed
                self.jump_speed -= self.gravity

                if self.jump_speed < -self.jump_height and self.pos.y > self.player_y:
                    self.is_jumping = False
                    self.jump_speed = self.jump_height
                    self.pos.y = self.player_y      
        else:
            self.direction.x = 0
            self.direction.y = 0

    def get_status(self):
    
        if '_' in self.status:
            self.status = self.status.split('_')[0]
        else:
            self.status = self.status


        action = ''

        if self.health_being_updated <= 0:
            action = '_death'
        else:

            if self.direction.x == 0 and self.direction.y == 0:
                if self.is_player_blast_attacking == False:
                    action = '_idle'
                elif self.is_player_blast_attacking == True:
                    action  = action.replace('_attack','_idle')
            
            if self.is_player_blast_attacking == True: # ----> The animation for attack 1) will be played only when the player is moving 2) The code for the animation is in the animate() function
                if 'idle' in action:
                    action = action.replace('_idle','_attack')
                else:
                    action = '_attack'

            if self.is_sword_selected == True:
                if 'idle' in action:
                    action = action.replace('_idle', '_sword_attack')
                else:
                    action = '_sword_attack'

            if self.has_player_collected_health_orb == True:
                if self.is_player_blast_attacking == False:
                    action = '_heal'
                else:
                    action = action.replace('_attack','_heal')

            if self.is_player_damaged == True:
                if self.is_player_blast_attacking == False:
                    action = '_hurt'
                else:
                    action = action.replace('_attack','_hurt')

        self.status = self.status + action


    def animate(self):
        if '_sword_attack' in self.status:
            self.animation_speed = 0.25
        elif self.is_sprinting: # Limiting going faster to these two states
            self.animation_speed = 0.25
        else:
            self.animation_speed = 0.15
        
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.is_sword_selected and 'sword_attack' in self.status:
            if self.frame_index >= len(animation) - 1:
                self.is_sword_selected = False
                self.frame_index = 0
        
        if self.frame_index >= len(animation):
            self.frame_index = 0


        if self.is_player_blast_attacking == True:  # ----> The reason as to why attack has its own animation is to ensure that the animation is not continuous, rather only one cycle is of the attack animation is played, and then the player goes back to idle or walk animation
            if self.frame_index >= len(animation) - 1:
                self.is_player_blast_attacking = False
                self.frame_index = 0

        if self.has_player_collected_health_orb == True: # ----> The reason as to why heal has its own animation is to ensure that the animation is not continuous, rather only one cycle is of the heal animation is played, and then the player goes back to idle or walk animation
            if self.frame_index >= len(animation) - 1:
                self.has_player_collected_health_orb = False
                self.frame_index = 0

        if '_hurt' in self.status:
            if self.frame_index >= len(animation) - 1:
                self.is_player_damaged = False
                self.frame_index = 0

        self.image = pygame.transform.scale((animation[int(self.frame_index)]),(150,150))
        self.screen.blit(self.image,self.rect)
        
        self.screen.blit(self.level_image,((self.MAX_WIDTH/2.7),(self.MAX_HEIGHT/9.9)))
        self.level_box_rect = self.level_image.get_rect(topleft = ((self.MAX_WIDTH/2.7),(self.MAX_HEIGHT/9.9)))


        level_text = self.level_font.render(f"LEVEL {self.level}", False, "white")
        self.screen.blit(level_text, ((self.MAX_WIDTH/2.23),(self.MAX_HEIGHT/8.5)))

            #DEBUG: Draw the Hitbox in Red and the Rect in Blue
      
        ## -- Instead of using fixed coordinates making it hard for the game to player on other laptops, we will be making calculations using the width of the screen -- ##
        
        ui_start_x = self.MAX_WIDTH - 400

        if self.is_sprinting == True:
            #pygame.draw.rect(self.screen, "green", self.rect, 2)   # The full sprite size
            self.screen.blit(self.when_running_image, (ui_start_x + 15,60))

        else:
            self.screen.blit(self.when_not_running_image, (ui_start_x + 15,60))
            pygame.draw.rect(self.screen, "blue", self.rect, 2) 
        

        if self.is_blue_blast_selected == False: # ---> Once a player selects an attack, the button for that attack will darken slightly, and the button for the other attack will remain bright, indicating that it is not selected.
            self.screen.blit(self.blue_blast_button_not_selected, (ui_start_x + 100,50))
        else:
            self.screen.blit(self.blue_blast_button_selected, (ui_start_x + 100,50))

        if self.is_purple_blast_selected == False:
            self.screen.blit(self.purple_blast_button_not_selected, (ui_start_x + 200,50))
        else:
            self.screen.blit(self.purple_blast_button_selected, (ui_start_x + 200,50))
       
        if self.is_sword_selected == False: # Drawing the sword buttons onto the screen.
            self.screen.blit(self.sword_button_not_selected, (ui_start_x + 300,50))
        else:
            self.screen.blit(self.sword_button_selected, (ui_start_x + 300,50))

    
        pygame.draw.rect(self.screen, "red", self.hitbox, 2)  # The actual collision area
        
        pygame.draw.rect(self.screen, "black", self.level_box_rect, 2)
            
    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize() #Stops trigonometry from affecting diagonal movement

        self.pos += self.direction * speed # Updates the actual positon of player on the screen

        if pygame.time.get_ticks() < self.slip_until:
            self.pos += self.slip_velocity
            self.slip_velocity *= 0.90
        else:
            self.slip_velocity.update(0,0)
        

        self.pos += self.knockback_velocity # --> This will happen only when the enemy is hit by the blast, 
        self.knockback_velocity *= 0.8 # --> Creates a deceleration effect, making things look smooth, this works as the self.knockback_velocity is changing when the enemy is hit by the blast.
        
        if self.knockback_velocity.length_squared() < 0.01: # --> A threshold to determine when to stop knockback effect.
            self.knockback_velocity.update(0, 0)

    def staying_in_screen(self):
        
        # Checking whether if player is crossing the screen horizontally #

        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > self.MAX_WIDTH - self.rect.width:
            self.pos.x = self.MAX_WIDTH - self.rect.width       

       # Checking whether if player is crossing the screen vertically #
        
        if self.pos.y < 0:
            self.pos.y = 0
        elif self.pos.y > self.MAX_HEIGHT - self.rect.height:
            self.pos.y = self.MAX_HEIGHT - self.rect.height

        self.rect.topleft = (self.pos.x, self.pos.y) #The picture frame should move to where the player actually is on screen
        self.hitbox.center = self.rect.center # Changing the physics part of player to the middle of the player picture frame

    def player_health(self): # --> Giving a proper health bar to the player, which changes based on how damaged the player gets.

        bar_width = 200 # --> Defining the elements for the health bar
        bar_height = 20
        margin = 20

        bar_x = self.MAX_WIDTH - bar_width - margin # --> For the bar to appear on the top right part of the screen
        bar_y = margin
      

        health_ratio = self.health_being_updated / self.health # --> The ratio of the health bar to the actual health of the player
        current_bar_width = bar_width * health_ratio # --> The current width of the health bar will be determined by the ratio of the health bar to the actual health of the player

        # 1) Drawing the red background of the health bar

        back_health_bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (20, 30, 20), back_health_bar_rect) #---> Rotting Earth Colour

        #2) Drawing the green foreground of the health bar

        if current_bar_width > 0:
            fore_health_bar_rect = pygame.Rect(bar_x, bar_y, current_bar_width, bar_height)
            pygame.draw.rect(self.screen, (39, 174, 96), fore_health_bar_rect) #---> Flask Vitality Green Colour
        
        # 3) Drawing the border of the health bar

        border_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (120, 120, 125), border_rect, 2) # ---> Tarnished Steel Grey Color

    def player_damage_health(self, enemy):
        enemy.update_scythe_projectile(self.hitbox.center) # --> To update the scythe's target as the player moves.

        # Enemy status must be in attack
        
        if hasattr(enemy, 'status'): # --> Necessary for debugging
            pass
            #print(enemy.status)
        else:
            print("Error: status is still not defined on this object!")

        damage = enemy.kick_attributes['Damage']
        knockback = enemy.kick_attributes['Knockback']
        knockback_multiplier = enemy.kick_attributes['Knockback_Multiplier']

        scythe_damage = enemy.scythe_attributes['Damage']
        scythe_knockback = enemy.scythe_attributes['Knockback']
        scythe_knockback_multiplier = enemy.scythe_attributes['Knockback_Multiplier']


        if self.health_being_updated > 0: # --> In the case that the player is not dead
            if enemy.kick_hit_frames[0] <= enemy.frame_index <= enemy.kick_hit_frames[1]: # --> The player only takes damage during the kick's hit frames.
                if 'attack' in enemy.status and 'scythe_attack' not in enemy.status: # Only considers the kicking animation
                    if self.hitbox.colliderect(enemy.hitbox) and not self.is_player_damaged: # --> Prevents repeat damage during the hurt animation.
                        self.health_being_updated -= damage
                        self.hurt_text = self.level_font.render(str(damage), False, 'red')
                        self.alpha = 255
                        self.hurt_text_y_offset = 0 # Both are in initial conditions, which are subject to change once the text is actually displayed.
                        self.getting_hurt_sound_effect.play()
                        self.is_player_damaged = True

                    # Knockback effect of the player
                        if self.rect.centerx != enemy.rect.centerx: # --> Knockback effect will only be applied if the enemy and player are not perfectly aligned vertically.
                            if self.rect.centerx > enemy.rect.centerx: # --> This stops the glitch where the player goes upwards.
                                    knockback_direction = 1  
                            else:
                                knockback_direction = -1
                        else: # --> If the enemy and player are perfectly aligned vertically, we determine what direction the player should be knocked back based on its current status (facing east or west).
                            if 'east' in self.status:
                                knockback_direction = -1
                            else:
                                knockback_direction = 1
                                
                        self.knockback_velocity.x += knockback_direction * knockback * knockback_multiplier 
                                # --> By how much the knockback velocity is increased depends on the distance by which the player goes back and the multiplier for player knockback. The multiplier is used to adjust the knockback effect based upon the attributes of the attack.
                                                           
        if enemy.scythe_in_flight and self.hitbox.colliderect(enemy.scythe_rect): # Now we consider the scythe attack of the enemy.
            enemy.scythe_in_flight = False
            if self.health_being_updated > 0 and not self.is_player_damaged:
                self.health_being_updated -= scythe_damage
                self.hurt_text = self.level_font.render(str(scythe_damage), False ,'red')
                self.alpha = 255
                self.hurt_text_y_offset = 0 # Both are in initial conditions, which are subject to change once the text is actually displayed.
                self.getting_hurt_sound_effect.play()

                self.is_player_damaged = True
                # Knockback effect of the player
               
                if self.rect.centerx > enemy.rect.centerx: # --> This stops the glitch where the player goes upwards.
                    knockback_direction = 1  
                else:
                    knockback_direction = -1

                # We don't need to consider when both rects are alligned, as the scythe attack wouldn't be activated at that point
                
                self.knockback_velocity.x += ( knockback_direction *scythe_knockback * scythe_knockback_multiplier)

    def blast_animation_and_sound_effects(self):
        # The intent with this subroutine is to handle which attack the player selects, playing its corresponding animation and also its sound effect
        # Blue Blast button --> E, Purple Blast button --> F
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()


        if keys[pygame.K_e]: # To select Blue Blast
            self.is_blue_blast_selected = True
            self.is_purple_blast_selected = False
        if keys[pygame.K_f]: # To select Purple Blast
            self.is_purple_blast_selected = True
            self.is_blue_blast_selected = False

        # --> Using boolean variables as a condition is much easier than relying on nested if statements.
        blast_key_down = keys[pygame.K_q]
        blast_key_pressed = blast_key_down and not self.blast_key_was_down
        self.blast_key_was_down = blast_key_down

        if blast_key_pressed:

            if self.is_blue_blast_selected == False and self.is_purple_blast_selected == False: # --> Player pressing attack button without selecting any attack, will be prompted to select an attack first.
                self.is_player_blast_attacking = False
                
                self.blast_status_text = self.level_font.render(f"Select an attack first!", False, "red")
                self.screen.blit(self.blast_status_text, ((self.MAX_WIDTH/2.5),(self.MAX_HEIGHT/3.5)))

            elif (not self.is_player_blast_attacking and not self.is_blast_released and current_time - self.last_blast_time >= self.blast_cooldown):
                self.is_player_blast_attacking = True
                self.is_blast_released = True
                self.last_blast_time = current_time
                self.blast_frame_index = 0
                self.blast_x = self.pos.x
                self.blast_y = self.pos.y
                self.blast_direction = 1 if self.blast_facing_right else -1
                self.blast_type = 'blue_blast' if self.is_blue_blast_selected else 'purple_blast'
                blast_attributes = getattr(self, f"{self.blast_type}_attributes") # --> Helps us in accessing the characteristics of each blast
                self.blast_velocity = blast_attributes["Speed"]
                self.blast_cooldown = blast_attributes["Cooldown"]
                
                if self.blast_type == 'blue_blast':
                    pygame.mixer.Channel(1).play(self.blue_blast)

                else:
                    pygame.mixer.Channel(2).play(self.purple_blast)
            else:
                self.blast_status_text = self.level_font.render("Blast is on cooldown!", False, "red")
                self.screen.blit(self.blast_status_text, ((self.MAX_WIDTH/2.5),(self.MAX_HEIGHT/3.5)))

        if self.last_blast_time > 0 and self.blast_cooldown > 0:
            cooldown_remaining = max(0, (self.blast_cooldown - (current_time - self.last_blast_time)) / 1000) # Getting the remaining cooldown time in seconds
            if cooldown_remaining > 0: # Essentially, for how long the cooldown remains.
                cooldown_text = self.level_font.render(f"Cooldown: {cooldown_remaining:.1f}s", False, "red") # The time remaining is rounded up to 1 dp to avoid cluttering the screen with long decimal numbers.
                self.screen.blit(cooldown_text, ((self.MAX_WIDTH/2.5),(self.MAX_HEIGHT/3.0))) # Place chosen via trial and error
        
        
        if self.is_blast_released:
            blast_animation = self.blast_animations.get(self.blast_type, [])
            if not blast_animation:
                self.is_blast_released = False
                return

            self.blast_frame_index = (self.blast_frame_index + self.blast_animation_speed) % len(blast_animation)
            self.blast_x += self.blast_velocity * self.blast_direction

            # Stop the blast once it has completely left the screen.
            if ((self.blast_direction == 1 and self.blast_x > self.MAX_WIDTH)
                    or (self.blast_direction == -1 and self.blast_x < -150)):
                self.is_blast_released = False
                return

            self.blast_image = pygame.transform.scale(
                blast_animation[int(self.blast_frame_index)], (150, 150))
            if self.blast_direction == 1:
                self.blast_image = pygame.transform.flip(self.blast_image, True, False)
            self.screen.blit(self.blast_image, (self.blast_x, self.blast_y))
      
    def collision_of_blast_with_enemy(self, enemy):
        if not self.is_blast_released: # The explosion can never occur if the blast is not released.
            return False

        blast_rect = pygame.Rect(self.blast_x, self.blast_y, 150, 150) # Aids us in finding the point of collision

        if not blast_rect.colliderect(enemy.hitbox): 
            return False # This is fed into the enemy_get_hurt_by_blast function to ensure that the enemy only takes damage when the blast collides with it.

        self.is_blast_released = False
        self.explosion_of_blast(enemy) # This is what leads to the explosion animation being played
        return True

    def collision_of_blast_with_wall(self):
        if not self.is_blast_released: # The explosion can never occur if the blast is not released.
            return False

        blast_rect = pygame.Rect(self.blast_x, self.blast_y, 150, 150) # Aids us in finding the point of collision

        if (blast_rect.left < 0 or blast_rect.right > self.MAX_WIDTH 
            or blast_rect.top < 0 or blast_rect.bottom > self.MAX_HEIGHT):
            self.is_blast_released = False
            self.explosion_of_blast(None) # This is what leads to the explosion animation being played
            return True
            
        return False

    def explosion_of_blast(self, enemy):
        if not self.is_explosion_active: # --> Foundations for which the explosion animation will be played by
            self.is_explosion_active = True
            self.explosion_frame_index = 0
            self.explosion_x = self.blast_x 
            self.explosion_y = self.blast_y

    def animation_of_explosion(self):
        if not self.is_explosion_active:
            return

        explosion_animation = self.blast_animations.get(f"{self.blast_type}_explosion", []) # --> Importing the relevant files for the explosion anmation of their respective blast type
        if not explosion_animation: # --> In case there are no animation files for the explosion animation, the explosion will not be played
            self.is_explosion_active = False
            return

        frame = int(self.explosion_frame_index)
        if self.explosion_frame_index == 0:
            sound_effect_to_be_played = self.__dict__.get(f"{self.blast_type}_explosion_sound_effect")
            if sound_effect_to_be_played:
                pygame.mixer.Channel(5).play(sound_effect_to_be_played)

        explosion_image = pygame.transform.scale(explosion_animation[frame], (150, 150)) # --> The original image is too small, and hence has to be scaled up to be more visible.
        self.screen.blit(explosion_image, (self.explosion_x, self.explosion_y))

        self.explosion_frame_index += 0.20 # --> Has to be faster than the speed of the blast itself for a more cohesive look.
        if self.explosion_frame_index >= len(explosion_animation): # --> Ensures that this animation is only played once.
            self.is_explosion_active = False
            self.explosion_frame_index = 0 # --> Helpful for the next time the animation is played as it will start from the beginning.

    def sword_attack(self,enemy): 
        keys = pygame.key.get_pressed()

        sword_key_down = keys[pygame.K_z]
        sword_key_pressed = sword_key_down and not self.sword_key_was_down
        self.sword_key_was_down = sword_key_down

        if sword_key_pressed and not self.is_sword_selected: # --> In case the sword button was already selected, so that no repeating sword attack / animations is played.  
            self.is_sword_selected = True
            self.frame_index = 0
            self.sword_hit_registered = False
            self.sword_strike.play()

        if (self.is_sword_selected and 'sword_attack' in self.status
                and not self.sword_hit_registered 
                and int(self.frame_index) == self.sword_hit_frame
                and self.hitbox.colliderect(enemy.hitbox)
                and self.status.split('_')[0] != enemy.status.split('_')[0]):

            self.sword_hit_registered = True # So now damage will be given to the enemy.
        
            return True
        # The return statements will be directed towards the enemy subroutine 'enemy_hurt_by_sword()'
        return False

    def apply_slip(self,strength = 30 ,duration_ms = 4500): # This function will occur based upon if conditions are met in droppable.py
        direction = self.direction.x

        self.slip_sound.play()
        if direction == 0:
            if 'east' in self.status:
                direction = 1
            else:
                direction = -1

        self.slip_velocity.x = direction * strength
        self.slip_until = pygame.time.get_ticks() + duration_ms

    def play_death(self):
        if self.health_being_updated <= 0:
            self.is_player_alive = False
            if not pygame.mixer.Channel(7).get_busy():
                pygame.mixer.Channel(7).play(self.player_death)
    
    def update(self):
        self.clock.tick(60)
        self.input()
        self.get_status()
        self.move(self.speed)        
        self.staying_in_screen()
        self.animate()
        self.player_health()
        self.play_death()
        if 'heal' not in self.status:
            self.blast_animation_and_sound_effects()
        self.animation_of_explosion()
        self.collision_of_blast_with_wall()
        if self.hurt_text is not None:
            self.alpha = max(0,self.alpha - self.frame_speed) # Text fades out slowly
            self.hurt_text_y_offset += self.frame_speed / 10 # The text slowly and slowly goes up as it fades
            self.hurt_text.set_alpha(self.alpha)
            self.screen.blit(self.hurt_text, (self.rect.x, (self.rect.y - 30 - self.hurt_text_y_offset))) # -30 for the text to be up at first, and then the offset makes it go further up.
            if self.alpha == 0:
                self.hurt_text = None

    def player_update(self,enemy):
        self.collision_of_blast_with_enemy(enemy)
        self.player_damage_health(enemy)